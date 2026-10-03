import 'dart:convert';

import 'package:http/http.dart' as http;

import '../shared/api_configuration.dart';
import '../shared/api_error.dart';
import '../usuarios/session_controller.dart';

class AdministracionApi {
  AdministracionApi({http.Client? client, SessionController? session, String? baseUrl})
    : _client = client ?? http.Client(),
      _session = session ?? SessionController.instance,
      baseUrl = baseUrl ?? defaultApiBaseUrl;
  final http.Client _client;
  final SessionController _session;
  final String baseUrl;

  Future<http.Response> _request(String method, String path, int expected, {Object? body}) async {
    final headers = _session.authorizedHeaders;
    final request = http.Request(method, Uri.parse('$baseUrl$path'));
    request.headers.addAll(headers);
    if (body != null) request.body = jsonEncode(body);
    final stream = await _client.send(request).timeout(const Duration(seconds: 20));
    final response = await http.Response.fromStream(stream).timeout(const Duration(seconds: 20));
    if (response.statusCode != expected) {
      if (response.statusCode == 401) _session.invalidateIfMatches(headers['Authorization']);
      throw ApiException(responseMessage(response), statusCode: response.statusCode);
    }
    return response;
  }

  Future<void> reportar(int publicacionId, String motivo) async {
    await _request('POST', '/administracion/reportes', 201,
      body: {'publicacion_id': publicacionId, 'motivo': motivo});
  }

  Future<List<Map<String, dynamic>>> pendientes() async {
    final response = await _request('GET', '/administracion/reportes', 200);
    return (jsonDecode(response.body) as List).cast<Map<String, dynamic>>();
  }

  Future<void> resolver(int reporteId, String decision, String nota) async {
    await _request('PATCH', '/administracion/reportes/$reporteId', 200,
      body: {'decision': decision, 'nota': nota});
  }

  void dispose() => _client.close();
}
