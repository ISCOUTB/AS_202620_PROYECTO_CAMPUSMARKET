import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

import '../shared/api_configuration.dart';
import '../shared/api_error.dart';
import '../usuarios/session_controller.dart';

class PublicacionTemporalmenteNoDisponible extends ApiException {
  const PublicacionTemporalmenteNoDisponible(super.message)
    : super(statusCode: 503);
  String get mensaje => message;
}

class ImagenPublicacion {
  const ImagenPublicacion({required this.nombre, required this.bytes});
  final String nombre;
  final Uint8List bytes;
}

class PublicacionesApi {
  PublicacionesApi({String? baseUrl, http.Client? client, SessionController? session})
    : baseUrl = baseUrl ?? defaultApiBaseUrl,
      _client = client ?? http.Client(),
      _session = session ?? SessionController.instance;

  final String baseUrl;
  final http.Client _client;
  final SessionController _session;

  Future<http.Response> _request(String method, String path, int expected, {Object? body}) async {
    final headers = _session.authorizedHeaders;
    final request = http.Request(method, Uri.parse('$baseUrl$path'));
    request.headers.addAll(headers);
    if (body != null) request.body = jsonEncode(body);
    final stream = await _client.send(request).timeout(const Duration(seconds: 20));
    final response = await http.Response.fromStream(stream).timeout(const Duration(seconds: 20));
    _check(response, expected, headers['Authorization']);
    return response;
  }

  void _check(http.Response response, int expected, String? authorization) {
    if (response.statusCode == expected) return;
    if (response.statusCode == 401) _session.invalidateIfMatches(authorization);
    if (response.statusCode == 503) {
      throw PublicacionTemporalmenteNoDisponible(responseMessage(response));
    }
    throw ApiException(responseMessage(response), statusCode: response.statusCode);
  }

  Map<String, dynamic> _payload(String titulo, String descripcion, double precio, String modalidad, String estado) =>
    {'titulo': titulo, 'descripcion': descripcion, 'precio': precio, 'modalidad': modalidad, 'estado': estado};

  Future<Map<String, dynamic>> crearPublicacion({
    required String titulo, required String descripcion, required double precio,
    required String modalidad, required String estado,
  }) async {
    final response = await _request('POST', '/publicaciones', 201,
      body: _payload(titulo, descripcion, precio, modalidad, estado));
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<List<Map<String, dynamic>>> listarMisPublicaciones() async {
    final response = await _request('GET', '/publicaciones/mias', 200);
    return (jsonDecode(response.body) as List).cast<Map<String, dynamic>>();
  }

  Future<Map<String, dynamic>> editarPublicacion({
    required int publicacionId, required String titulo, required String descripcion,
    required double precio, required String modalidad, required String estado,
  }) async {
    final response = await _request('PUT', '/publicaciones/$publicacionId', 200,
      body: _payload(titulo, descripcion, precio, modalidad, estado));
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> cambiarEstadoPublicacion({
    required int publicacionId, required String estadoPublicacion,
  }) async {
    final response = await _request('PATCH', '/publicaciones/$publicacionId/estado', 200,
      body: {'estado_publicacion': estadoPublicacion});
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<void> eliminarPublicacion(int publicacionId) async {
    await _request('DELETE', '/publicaciones/$publicacionId', 204);
  }

  Future<Map<String, dynamic>> subirImagen({
    required int publicacionId, required ImagenPublicacion imagen,
  }) async {
    final headers = _session.authorizedHeaders;
    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/publicaciones/$publicacionId/imagenes'));
    request.headers['Authorization'] = headers['Authorization']!;
    request.files.add(http.MultipartFile.fromBytes('archivo', imagen.bytes, filename: imagen.nombre));
    final stream = await _client.send(request).timeout(const Duration(seconds: 30));
    final response = await http.Response.fromStream(stream).timeout(const Duration(seconds: 20));
    _check(response, 201, headers['Authorization']);
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<void> subirImagenes({required int publicacionId, required List<ImagenPublicacion> imagenes}) async {
    if (imagenes.length > 3) throw ArgumentError('Solo se permiten hasta 3 imágenes.');
    for (final imagen in imagenes) {
      await subirImagen(publicacionId: publicacionId, imagen: imagen);
    }
  }

  Future<void> eliminarImagen(int publicacionId, int imagenId) async {
    await _request('DELETE', '/publicaciones/$publicacionId/imagenes/$imagenId', 204);
  }

  Future<void> elegirPrincipal(int publicacionId, int imagenId) async {
    await _request('PUT', '/publicaciones/$publicacionId/imagenes/$imagenId/principal', 200);
  }

  Future<List<dynamic>> listarPublicaciones() async {
    final response = await _client.get(Uri.parse('$baseUrl/publicaciones')).timeout(const Duration(seconds: 20));
    _check(response, 200, null);
    return jsonDecode(response.body) as List<dynamic>;
  }
}
