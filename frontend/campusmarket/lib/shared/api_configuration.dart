import 'package:flutter/foundation.dart';

const configuredApiBaseUrl = String.fromEnvironment('CAMPUSMARKET_API_BASE_URL');

String get defaultApiBaseUrl {
  if (configuredApiBaseUrl.isNotEmpty) {
    return configuredApiBaseUrl.replaceFirst(RegExp(r'/$'), '');
  }
  if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
    return 'http://10.0.2.2:8000';
  }
  return 'http://localhost:8000';
}
