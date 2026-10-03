import 'package:campusmarket/usuarios/auth_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  for (final size in [const Size(375, 812), const Size(1440, 1000)]) {
    testWidgets('registro se adapta al viewport y valida antes de llamar a la API: $size', (tester) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(const MaterialApp(home: AuthPage(registroInicial: true)));
      final submit = find.byKey(const Key('auth-enviar'));
      await tester.ensureVisible(submit);
      await tester.tap(submit);
      await tester.pump();
      expect(find.text('Ingresa un nombre de al menos 2 caracteres.'), findsOneWidget);
      expect(find.text('Ingresa un correo electrónico válido.'), findsOneWidget);
      expect(find.text('La contraseña debe tener entre 12 y 128 caracteres.'), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  }
}
