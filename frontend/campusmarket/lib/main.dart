import 'package:flutter/material.dart';

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
      home: Scaffold(
        appBar: AppBar(title: const Text('CampusMarket')),
        body: const Center(
          child: Text(
            'Bienvenido a CampusMarket',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }
}
