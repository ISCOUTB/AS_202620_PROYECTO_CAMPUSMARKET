import 'package:flutter/material.dart';

import 'publicaciones/publicacion_form_page.dart';


void main() {
  runApp(const CampusMarketApp());
}


class CampusMarketApp extends StatelessWidget {
  const CampusMarketApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CampusMarket',
      theme: ThemeData(useMaterial3: true),
      home: const PublicacionFormPage(),
    );
  }
}
