import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  const ApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;
  @override
  String toString() => message;
}

String responseMessage(http.Response response) {
  try {
    final body = jsonDecode(response.body);
    if (body is Map && body['detail'] is String) {
      return body['detail'] as String;
    }
  } catch (_) {
    // An invalid response never becomes raw server output in the interface.
  }
  return switch (response.statusCode) {
    401 => 'Tu sesión terminó. Inicia sesión nuevamente.',
    403 => 'Tu cuenta no tiene permiso para esta acción.',
    404 => 'La publicación no existe o no te pertenece.',
    409 => 'Esta acción ya fue registrada.',
    422 => 'Revisa los campos y sus límites antes de continuar.',
    429 => 'Demasiados intentos. Espera cinco minutos e intenta nuevamente.',
    503 => 'El servicio está temporalmente no disponible. Intenta nuevamente.',
    _ => 'No fue posible completar la operación. Intenta nuevamente.',
  };
}

String readableError(Object error) => error is ApiException
    ? error.message
    : 'No fue posible conectar. Revisa tu conexión e intenta nuevamente.';
