import 'dart:convert';

import 'package:campusmarket/publicaciones/publicaciones_api.dart';
import 'package:campusmarket/shared/api_error.dart';
import 'package:campusmarket/usuarios/session_controller.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

http.Response sessionResponse(String token, int id) => http.Response(jsonEncode({
  'access_token': token, 'token_type': 'bearer',
  'expira_en': DateTime.now().toUtc().add(const Duration(hours: 1)).toIso8601String(),
  'usuario': {'id': id, 'nombre': 'Cuenta de prueba', 'correo': 'cuenta@example.test', 'es_admin': false},
}), 200);

void main() {
  test('crear y consultar propias envía sesión y omite cualquier propietario suministrado', () async {
    final session = SessionController(client: MockClient((_) async => sessionResponse('fixture-A', 41)));
    addTearDown(session.dispose);
    await session.login(correo: 'cuenta@example.test', password: 'Solo para un fixture');
    final requests = <http.Request>[];
    final api = PublicacionesApi(session: session, client: MockClient((request) async {
      requests.add(request);
      return http.Response(request.method == 'POST' ? '{"id":71}' : '[]', request.method == 'POST' ? 201 : 200);
    }));
    await api.crearPublicacion(titulo: 'Libro', descripcion: 'Buen estado', precio: 25000, modalidad: 'venta', estado: 'usado');
    await api.listarMisPublicaciones();
    expect(requests, hasLength(2));
    for (final request in requests) {
      expect(request.headers['Authorization'], session.authorizedHeaders['Authorization']);
      expect(request.url.queryParameters, isNot(contains('propietario_id')));
    }
    expect(jsonDecode(requests.first.body), isNot(contains('propietario_id')));
  });

  test('logout fallido conserva sesión y logout confirmado la revoca en el cliente', () async {
    var unavailable = true;
    final session = SessionController(client: MockClient((request) async {
      if (request.url.path.endsWith('/login')) return sessionResponse('fixture-A', 41);
      return http.Response('', unavailable ? 503 : 204);
    }));
    addTearDown(session.dispose);
    await session.login(correo: 'cuenta@example.test', password: 'Solo para un fixture');
    await expectLater(session.logout(), throwsA(isA<ApiException>()));
    expect(session.authenticated, isTrue);
    unavailable = false;
    await session.logout();
    expect(session.usuario, isNull);
    expect(() => session.authorizedHeaders, throwsA(isA<ApiException>()));
  });

  test('respuesta antigua de A no invalida una sesión nueva de B', () async {
    var current = 41;
    final session = SessionController(client: MockClient((_) async => sessionResponse('fixture-$current', current)));
    addTearDown(session.dispose);
    await session.login(correo: 'a@example.test', password: 'Solo para un fixture');
    final previous = session.authorizedHeaders['Authorization'];
    current = 42;
    await session.login(correo: 'b@example.test', password: 'Solo para un fixture');
    session.invalidateIfMatches(previous);
    expect(session.authenticated, isTrue);
    expect(session.usuario?.id, 42);
    session.invalidateIfMatches(session.authorizedHeaders['Authorization']);
    expect(session.authenticated, isFalse);
  });

  test('un 401 en gestión elimina la sesión que originó la petición', () async {
    final session = SessionController(client: MockClient((_) async => sessionResponse('fixture-A', 41)));
    addTearDown(session.dispose);
    await session.login(correo: 'cuenta@example.test', password: 'Solo para un fixture');
    final api = PublicacionesApi(session: session, client: MockClient((_) async => http.Response('', 401)));
    await expectLater(api.listarMisPublicaciones(), throwsA(isA<ApiException>()));
    expect(session.authenticated, isFalse);
  });
}
