import 'dart:convert';

import 'package:http/http.dart' as http;

import 'publicacion_catalogo.dart';

class CatalogoApi {
  const CatalogoApi({String? baseUrl}) : baseUrl = baseUrl ?? _configuredBaseUrl;

  static const _configuredBaseUrl = String.fromEnvironment(
    'CAMPUSMARKET_API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  final String baseUrl;

  Future<List<PublicacionCatalogo>> buscar({
    String? texto,
    String? modalidad,
    String? estado,
    double? precioMin,
    double? precioMax,
  }) async {
    final query = <String, String>{};

    if (texto != null && texto.trim().isNotEmpty) {
      query['q'] = texto.trim();
    }

    if (modalidad != null && modalidad.isNotEmpty) {
      query['modalidad'] = modalidad;
    }

    if (estado != null && estado.isNotEmpty) {
      query['estado'] = estado;
    }

    if (precioMin != null) {
      query['precio_min'] = precioMin.toString();
    }

    if (precioMax != null) {
      query['precio_max'] = precioMax.toString();
    }

    final uri = Uri.parse(
      '$baseUrl/catalogo',
    ).replace(queryParameters: query.isEmpty ? null : query);

    final response = await http.get(uri);

    if (response.statusCode != 200) {
      throw Exception(
        'No se pudo consultar el catálogo (${response.statusCode}).',
      );
    }

    final data = jsonDecode(response.body) as List<dynamic>;

    return data
        .map(
          (item) => PublicacionCatalogo.fromJson(
            item as Map<String, dynamic>,
            baseUrl: baseUrl,
          ),
        )
        .toList();
  }

  Future<PublicacionCatalogo> obtenerDetalle(int id) async {
    final response = await http.get(Uri.parse('$baseUrl/catalogo/$id'));

    if (response.statusCode == 404) {
      throw Exception('La publicación no existe.');
    }

    if (response.statusCode != 200) {
      throw Exception(
        'No se pudo consultar la publicación (${response.statusCode}).',
      );
    }

    return PublicacionCatalogo.fromJson(
      jsonDecode(response.body) as Map<String, dynamic>,
      baseUrl: baseUrl,
    );
  }
}
