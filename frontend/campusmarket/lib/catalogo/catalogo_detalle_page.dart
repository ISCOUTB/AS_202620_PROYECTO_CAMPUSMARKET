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

                final visual = _GaleriaPublicacion(
                  publicacion: publicacion,
                  height: desktop ? 480 : 320,
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

class _GaleriaPublicacion extends StatelessWidget {
  const _GaleriaPublicacion({
    required this.publicacion,
    required this.height,
  });

  final PublicacionCatalogo publicacion;
  final double height;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final imagenes = publicacion.imagenes;

    if (imagenes.isEmpty) {
      return Container(
        height: height,
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
            size: 110,
            color: colors.primary,
          ),
        ),
      );
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(28),
      child: SizedBox(
        height: height,
        child: Stack(
          children: [
            PageView.builder(
              itemCount: imagenes.length,
              itemBuilder: (context, index) {
                final imagen = imagenes[index];

                return Image.network(
                  imagen.imagenUrl,
                  width: double.infinity,
                  height: height,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return ColoredBox(
                      color: colors.surfaceContainerHighest,
                      child: Center(
                        child: Icon(
                          Icons.broken_image_outlined,
                          size: 72,
                          color: colors.onSurfaceVariant,
                        ),
                      ),
                    );
                  },
                );
              },
            ),
            if (imagenes.length > 1)
              Positioned(
                right: 16,
                bottom: 16,
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    color: colors.surface.withValues(alpha: 0.88),
                    borderRadius: BorderRadius.circular(999),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 7,
                    ),
                    child: Text(
                      '${imagenes.length} fotos · desliza para verlas',
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
