import 'dart:convert';

import 'package:campusmarket/publicaciones/publicaciones_api.dart';
import 'package:campusmarket/usuarios/session_controller.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

void main() {
  test('reintento envía la misma clave; publicación nueva usa otra', () async {
    final session = SessionController(
      client: MockClient(
        (_) async => http.Response(
          jsonEncode({
            'access_token': 'fixture-token',
            'token_type': 'bearer',
            'expira_en': DateTime.now()
                .toUtc()
                .add(const Duration(hours: 1))
                .toIso8601String(),
            'usuario': {
              'id': 41,
              'nombre': 'Prueba',
              'correo': 'prueba@example.test',
              'es_admin': false,
            },
          }),
          200,
        ),
      ),
    );
    addTearDown(session.dispose);
    await session.login(
      correo: 'prueba@example.test',
      password: 'clave-de-prueba',
    );
    final requests = <http.Request>[];
    final api = PublicacionesApi(
      session: session,
      client: MockClient((request) async {
        requests.add(request);
        return http.Response('{"id":71}', 201);
      }),
    );
    addTearDown(api.dispose);

    Future<void> crear(String key) => api
        .crearPublicacion(
          titulo: 'Libro',
          descripcion: 'En buen estado',
          precio: 25000,
          modalidad: 'venta',
          estado: 'usado',
          idempotencyKey: key,
        )
        .then((_) {});

    await crear('intento-0001');
    await crear('intento-0001');
    await crear('intento-0002');

    expect(requests, hasLength(3));
    expect(requests.map((r) => r.headers['Idempotency-Key']).toList(), [
      'intento-0001',
      'intento-0001',
      'intento-0002',
    ]);
    expect(requests[0].body, requests[1].body);
    expect(jsonDecode(requests[0].body), isNot(contains('idempotencyKey')));
  });
}
