import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:integration_test/integration_test_driver_extended.dart';

Future<void> main() async {
  final directory = Directory('../../artifacts/e2e')..createSync(recursive: true);
  await runZoned(
    () => integrationDriver(
      onScreenshot: (name, bytes, [args]) async {
        await File('${directory.path}/$name.png').writeAsBytes(bytes);
        return bytes.isNotEmpty;
      },
      responseDataCallback: (data) async {
        final evidence = {
          'hash': Platform.environment['GITHUB_SHA'],
          'checks': data?['checks'],
          'platform': data?['platform'],
          'viewport': data?['viewport'],
          'screenshots': (data?['screenshots'] as List?)
              ?.map((item) => item['screenshotName']).toList(),
        };
        await File('${directory.path}/resultado.json').writeAsString(jsonEncode(evidence));
        stdout.writeln('CAMPUSMARKET_E2E_RESULT=${jsonEncode(evidence)}');
      },
      writeResponseOnFailure: true,
    ),
    zoneSpecification: ZoneSpecification(
      print: (self, parent, zone, message) {
        if (message.startsWith('result ')) {
          parent.print(zone, 'Resultado del flujo recibido; capturas guardadas sin imprimir sus bytes.');
        } else {
          parent.print(zone, message);
        }
      },
    ),
  );
}
