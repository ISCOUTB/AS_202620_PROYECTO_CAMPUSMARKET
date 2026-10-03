import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

class PublicacionTemporalmenteNoDisponible implements Exception {
  const PublicacionTemporalmenteNoDisponible(this.mensaje);

  final String mensaje;

  @override
  String toString() => mensaje;
}

class ImagenPublicacion {
  const ImagenPublicacion({required this.nombre, required this.bytes});

  final String nombre;
  final Uint8List bytes;
}

class PublicacionesApi {
  PublicacionesApi({String? baseUrl}) : baseUrl = baseUrl ?? _configuredBaseUrl;

  static const String _configuredBaseUrl = String.fromEnvironment(
    'CAMPUSMARKET_API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  static const int propietarioActual = 1;

  final String baseUrl;

  Future<Map<String, dynamic>> crearPublicacion({
    required String titulo,
    required String descripcion,
    required double precio,
    required String modalidad,
    required String estado,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/publicaciones'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'titulo': titulo,
        'descripcion': descripcion,
        'precio': precio,
        'modalidad': modalidad,
        'estado': estado,
        'propietario_id': propietarioActual,
      }),
    );

    _throwIfUnavailable(response);

    if (response.statusCode != 201) {
      throw Exception('No fue posible crear la publicación.');
    }

    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<List<Map<String, dynamic>>> listarMisPublicaciones() async {
    final response = await http.get(
      Uri.parse(
        '$baseUrl/publicaciones/mias?propietario_id=$propietarioActual',
      ),
    );

    _throwIfUnavailable(response);

    if (response.statusCode != 200) {
      throw Exception('No fue posible consultar tus publicaciones.');
    }

    final data = jsonDecode(response.body) as List<dynamic>;
    return data.cast<Map<String, dynamic>>();
  }

  Future<Map<String, dynamic>> editarPublicacion({
    required int publicacionId,
    required String titulo,
    required String descripcion,
    required double precio,
    required String modalidad,
    required String estado,
  }) async {
    final response = await http.put(
      Uri.parse(
        '$baseUrl/publicaciones/$publicacionId'
        '?propietario_id=$propietarioActual',
      ),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'titulo': titulo,
        'descripcion': descripcion,
        'precio': precio,
        'modalidad': modalidad,
        'estado': estado,
      }),
    );

    _throwIfUnavailable(response);

    if (response.statusCode == 404) {
      throw Exception('La publicación no existe o no te pertenece.');
    }

    if (response.statusCode != 200) {
      throw Exception('No fue posible editar la publicación.');
    }

    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> cambiarEstadoPublicacion({
    required int publicacionId,
    required String estadoPublicacion,
  }) async {
    final response = await http.patch(
      Uri.parse(
        '$baseUrl/publicaciones/$publicacionId/estado'
        '?propietario_id=$propietarioActual',
      ),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'estado_publicacion': estadoPublicacion}),
    );

    _throwIfUnavailable(response);

    if (response.statusCode == 404) {
      throw Exception('La publicación no existe o no te pertenece.');
    }

    if (response.statusCode != 200) {
      throw Exception('No fue posible cambiar el estado.');
    }

    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<void> eliminarPublicacion(int publicacionId) async {
    final response = await http.delete(
      Uri.parse(
        '$baseUrl/publicaciones/$publicacionId'
        '?propietario_id=$propietarioActual',
      ),
    );

    _throwIfUnavailable(response);

    if (response.statusCode == 404) {
      throw Exception('La publicación no existe o no te pertenece.');
    }

    if (response.statusCode != 204) {
      throw Exception('No fue posible eliminar la publicación.');
    }
  }

  Future<Map<String, dynamic>> subirImagen({
    required int publicacionId,
    required ImagenPublicacion imagen,
  }) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/publicaciones/$publicacionId/imagenes'),
    );

    request.files.add(
      http.MultipartFile.fromBytes(
        'archivo',
        imagen.bytes,
        filename: imagen.nombre,
      ),
    );

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 400) {
      final body = jsonDecode(response.body);
      throw Exception(
        body is Map<String, dynamic>
            ? body['detail']?.toString() ?? 'La imagen no es válida.'
            : 'La imagen no es válida.',
      );
    }

    if (response.statusCode == 404) {
      throw Exception('La publicación no existe.');
    }

    _throwIfUnavailable(response);

    if (response.statusCode != 201) {
      throw Exception('No fue posible subir la imagen.');
    }

    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<void> subirImagenes({
    required int publicacionId,
    required List<ImagenPublicacion> imagenes,
  }) async {
    if (imagenes.length > 3) {
      throw ArgumentError('Solo se permiten hasta 3 imágenes.');
    }

    for (final imagen in imagenes) {
      await subirImagen(publicacionId: publicacionId, imagen: imagen);
    }
  }

  Future<List<dynamic>> listarPublicaciones() async {
    final response = await http.get(Uri.parse('$baseUrl/publicaciones'));

    _throwIfUnavailable(response);

    if (response.statusCode != 200) {
      throw Exception('No fue posible consultar las publicaciones.');
    }

    return jsonDecode(response.body) as List<dynamic>;
  }

  void _throwIfUnavailable(http.Response response) {
    if (response.statusCode != 503) return;

    String? detail;
    try {
      final body = jsonDecode(response.body);
      if (body is Map<String, dynamic>) {
        detail = body['detail']?.toString();
      }
    } catch (_) {
      detail = null;
    }

    throw PublicacionTemporalmenteNoDisponible(
      detail ??
          'La persistencia está temporalmente no disponible. '
              'Intenta nuevamente.',
    );
  }
}
