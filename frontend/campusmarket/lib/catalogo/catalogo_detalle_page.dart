import 'package:flutter/material.dart';

import 'publicacion_catalogo.dart';

class CatalogoDetallePage extends StatelessWidget {
  const CatalogoDetallePage({required this.publicacion, super.key});

  final PublicacionCatalogo publicacion;

  String _precio(double value) {
    return value.truncateToDouble() == value
        ? '\$${value.toStringAsFixed(0)}'
        : '\$${value.toStringAsFixed(2)}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('Detalle de publicación')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 1100),
            child: LayoutBuilder(
              builder: (context, constraints) {
                final desktop = constraints.maxWidth >= 800;

                final visual = Container(
                  height: desktop ? 480 : 300,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(28),
                    gradient: LinearGradient(
                      colors: [
                        colors.primaryContainer,
                        colors.surfaceContainerHighest,
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Center(
                    child: Icon(
                      Icons.shopping_bag_outlined,
                      size: desktop ? 120 : 80,
                      color: colors.primary,
                    ),
                  ),
                );

                final informacion = Padding(
                  padding: EdgeInsets.only(
                    left: desktop ? 40 : 0,
                    top: desktop ? 0 : 28,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          Chip(
                            avatar: const Icon(
                              Icons.verified_outlined,
                              size: 18,
                            ),
                            label: Text(publicacion.estado),
                          ),
                          Chip(
                            avatar: Icon(
                              publicacion.modalidad == 'venta'
                                  ? Icons.sell_outlined
                                  : Icons.key_outlined,
                              size: 18,
                            ),
                            label: Text(publicacion.modalidad),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),
                      Text(
                        publicacion.titulo,
                        style: theme.textTheme.displaySmall?.copyWith(
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        _precio(publicacion.precio),
                        style: theme.textTheme.headlineLarge?.copyWith(
                          color: colors.primary,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const SizedBox(height: 30),
                      Text(
                        'Descripción',
                        style: theme.textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        publicacion.descripcion,
                        style: theme.textTheme.bodyLarge?.copyWith(
                          height: 1.6,
                          color: colors.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(height: 32),
                      SizedBox(
                        width: double.infinity,
                        child: FilledButton.icon(
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text(
                                  'El contacto entre usuarios se implementará cuando exista su contrato backend.',
                                ),
                              ),
                            );
                          },
                          icon: const Icon(Icons.chat_bubble_outline),
                          label: const Padding(
                            padding: EdgeInsets.symmetric(vertical: 15),
                            child: Text('Contactar'),
                          ),
                        ),
                      ),
                    ],
                  ),
                );

                if (desktop) {
                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(flex: 6, child: visual),
                      Expanded(flex: 5, child: informacion),
                    ],
                  );
                }

                return Column(children: [visual, informacion]);
              },
            ),
          ),
        ),
      ),
    );
  }
}
