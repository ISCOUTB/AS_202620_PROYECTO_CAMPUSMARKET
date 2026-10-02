import 'package:flutter/material.dart';

import '../publicacion_catalogo.dart';

class CatalogoCard extends StatelessWidget {
  const CatalogoCard({
    required this.publicacion,
    required this.onTap,
    super.key,
  });

  final PublicacionCatalogo publicacion;
  final VoidCallback onTap;

  String _formatearPrecio(double value) {
    final entero = value.truncateToDouble() == value;

    return entero
        ? '\$${value.toStringAsFixed(0)}'
        : '\$${value.toStringAsFixed(2)}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final imagenPrincipal = publicacion.imagenPrincipal;

    return Card(
      clipBehavior: Clip.antiAlias,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(
          color: colorScheme.outlineVariant.withValues(alpha: 0.7),
        ),
      ),
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: 180,
              width: double.infinity,
              child: imagenPrincipal == null
                  ? _PlaceholderImagen(colorScheme: colorScheme)
                  : Image.network(
                      imagenPrincipal.imagenUrl,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return _PlaceholderImagen(colorScheme: colorScheme);
                      },
                    ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        _Etiqueta(
                          texto: publicacion.estado,
                          icono: Icons.verified_outlined,
                        ),
                        const Spacer(),
                        Icon(
                          publicacion.modalidad == 'venta'
                              ? Icons.sell_outlined
                              : Icons.key_outlined,
                          size: 18,
                          color: colorScheme.primary,
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      publicacion.titulo,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      _formatearPrecio(publicacion.precio),
                      style: theme.textTheme.headlineSmall?.copyWith(
                        color: colorScheme.primary,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      publicacion.descripcion,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: colorScheme.onSurfaceVariant,
                      ),
                    ),
                    const Spacer(),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: onTap,
                        icon: const Icon(Icons.visibility_outlined),
                        label: const Text('Ver detalles'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PlaceholderImagen extends StatelessWidget {
  const _PlaceholderImagen({required this.colorScheme});

  final ColorScheme colorScheme;

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            colorScheme.primaryContainer,
            colorScheme.surfaceContainerHighest,
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Center(
        child: Icon(
          Icons.shopping_bag_outlined,
          size: 58,
          color: colorScheme.primary,
        ),
      ),
    );
  }
}

class _Etiqueta extends StatelessWidget {
  const _Etiqueta({required this.texto, required this.icono});

  final String texto;
  final IconData icono;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: colorScheme.secondaryContainer,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icono, size: 15, color: colorScheme.onSecondaryContainer),
          const SizedBox(width: 5),
          Text(
            texto[0].toUpperCase() + texto.substring(1),
            style: TextStyle(
              color: colorScheme.onSecondaryContainer,
              fontWeight: FontWeight.w600,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}
