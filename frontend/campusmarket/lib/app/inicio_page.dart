import 'package:flutter/material.dart';

import '../shared/formatters.dart';
import '../catalogo/catalogo_api.dart';
import '../catalogo/catalogo_detalle_page.dart';
import '../catalogo/publicacion_catalogo.dart';
import '../catalogo/widgets/catalogo_card.dart';

class InicioPage extends StatefulWidget {
  const InicioPage({
    required this.onIrCatalogo,
    required this.onIrPublicar,
    super.key,
  });

  final VoidCallback onIrCatalogo;
  final VoidCallback onIrPublicar;

  @override
  State<InicioPage> createState() => _InicioPageState();
}

class _InicioPageState extends State<InicioPage> {
  final _api = const CatalogoApi();

  List<PublicacionCatalogo> _publicaciones = [];
  bool _cargando = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _cargar();
  }

  Future<void> _cargar() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final resultado = await _api.buscar();

      if (!mounted) {
        return;
      }

      setState(() {
        _publicaciones = resultado.take(4).toList();
      });
    } catch (error) {
      if (!mounted) {
        return;
      }

      setState(() {
        _error = error.toString();
      });
    } finally {
      if (mounted) {
        setState(() {
          _cargando = false;
        });
      }
    }
  }

  PublicacionCatalogo? get _destacada {
    for (final publicacion in _publicaciones) {
      if (publicacion.imagenPrincipal != null) return publicacion;
    }
    return null;
  }

  void _abrirDetalle(PublicacionCatalogo publicacion) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => CatalogoDetallePage(publicacion: publicacion),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Scaffold(
      backgroundColor: colors.surface,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 24, 24, 40),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1400),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _HeroInicio(
                    destacada: _destacada,
                    onAbrirDestacada: _destacada == null ? null : () => _abrirDetalle(_destacada!),
                    onIrCatalogo: widget.onIrCatalogo,
                    onIrPublicar: widget.onIrPublicar,
                  ),
                  const SizedBox(height: 28),
                  const _BeneficiosInicio(),
                  const SizedBox(height: 36),
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Publicaciones recientes',
                              style: theme.textTheme.headlineSmall?.copyWith(
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Productos publicados actualmente en CampusMarket.',
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: colors.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ),
                      ),
                      TextButton.icon(
                        onPressed: widget.onIrCatalogo,
                        icon: const Icon(Icons.arrow_forward),
                        label: const Text('Ver catálogo'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  _buildPublicaciones(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPublicaciones() {
    final colors = Theme.of(context).colorScheme;

    if (_cargando) {
      return const SizedBox(
        height: 260,
        child: Center(child: CircularProgressIndicator()),
      );
    }

    if (_error != null) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.all(28),
        decoration: BoxDecoration(
          color: colors.errorContainer.withValues(alpha: 0.35),
          borderRadius: BorderRadius.circular(24),
        ),
        child: Column(
          children: [
            Icon(Icons.cloud_off_outlined, color: colors.error, size: 42),
            const SizedBox(height: 12),
            const Text(
              'No fue posible cargar las publicaciones recientes.',
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 14),
            OutlinedButton.icon(
              onPressed: _cargar,
              icon: const Icon(Icons.refresh),
              label: const Text('Reintentar'),
            ),
          ],
        ),
      );
    }

    if (_publicaciones.isEmpty) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.all(32),
        decoration: BoxDecoration(
          color: colors.surfaceContainerLow,
          borderRadius: BorderRadius.circular(24),
        ),
        child: const Column(
          children: [
            Icon(Icons.inventory_2_outlined, size: 46),
            SizedBox(height: 12),
            Text('Todavía no hay publicaciones disponibles.'),
          ],
        ),
      );
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        var columnas = 1;
        if (constraints.maxWidth >= 1180) {
          columnas = 4;
        } else if (constraints.maxWidth >= 820) {
          columnas = 3;
        } else if (constraints.maxWidth >= 560) {
          columnas = 2;
        }

        return GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _publicaciones.length,
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columnas,
            crossAxisSpacing: 18,
            mainAxisSpacing: 18,
            childAspectRatio: columnas == 1 ? 0.62 : 0.72,
          ),
          itemBuilder: (context, index) {
            final publicacion = _publicaciones[index];
            return CatalogoCard(
              publicacion: publicacion,
              onTap: () => _abrirDetalle(publicacion),
            );
          },
        );
      },
    );
  }
}

class _HeroInicio extends StatelessWidget {
  const _HeroInicio({
    required this.onIrCatalogo,
    required this.onIrPublicar,
    this.destacada,
    this.onAbrirDestacada,
  });

  final VoidCallback onIrCatalogo;
  final VoidCallback onIrPublicar;
  final PublicacionCatalogo? destacada;
  final VoidCallback? onAbrirDestacada;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        gradient: LinearGradient(
          colors: [
            colors.primaryContainer,
            colors.surfaceContainerHighest,
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: LayoutBuilder(
        builder: (context, constraints) {
          final compacto = constraints.maxWidth < 820;

          final contenido = Padding(
            padding: EdgeInsets.all(compacto ? 24 : 38),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 7,
                  ),
                  decoration: BoxDecoration(
                    color: colors.surface.withValues(alpha: 0.9),
                    borderRadius: BorderRadius.circular(999),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.groups_outlined, size: 17, color: colors.primary),
                      const SizedBox(width: 7),
                      const Text(
                        'Comunidad universitaria',
                        style: TextStyle(fontWeight: FontWeight.w700),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  'Tu próximo hallazgo\nestá en el campus',
                  style: theme.textTheme.displaySmall?.copyWith(
                    fontWeight: FontWeight.w900,
                    height: 1.04,
                  ),
                ),
                const SizedBox(height: 16),
                ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 650),
                  child: Text(
                    'Libros, tecnología y mucho más, de estudiante a estudiante. '
                    'Encuentra lo que necesitas y dale una segunda vida a lo que ya no usas.',
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: colors.onSurfaceVariant,
                      height: 1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 26),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    FilledButton.icon(
                      onPressed: onIrCatalogo,
                      icon: const Icon(Icons.storefront_outlined),
                      label: const Text('Explorar catálogo'),
                    ),
                    OutlinedButton.icon(
                      onPressed: onIrPublicar,
                      icon: const Icon(Icons.add_circle_outline),
                      label: const Text('Publicar producto'),
                    ),
                  ],
                ),
              ],
            ),
          );

          final visual = Padding(
            padding: EdgeInsets.fromLTRB(
              compacto ? 24 : 0,
              compacto ? 0 : 24,
              compacto ? 24 : 24,
              24,
            ),
            child: Container(
              constraints: BoxConstraints(minHeight: compacto ? 210 : 330),
              decoration: BoxDecoration(
                color: colors.surface.withValues(alpha: 0.92),
                borderRadius: BorderRadius.circular(26),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.06),
                    blurRadius: 24,
                    offset: const Offset(0, 12),
                  ),
                ],
              ),
              child: destacada?.imagenPrincipal != null
                  ? _HallazgoDestacado(publicacion: destacada!, onTap: onAbrirDestacada)
                  : Stack(
                children: [
                  Positioned(
                    right: -40,
                    top: -40,
                    child: _Burbuja(
                      size: 180,
                      color: colors.primaryContainer,
                    ),
                  ),
                  Positioned(
                    left: -30,
                    bottom: -50,
                    child: _Burbuja(
                      size: 150,
                      color: colors.secondaryContainer,
                    ),
                  ),
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.all(32),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 86,
                            height: 86,
                            decoration: BoxDecoration(
                              color: colors.primary,
                              borderRadius: BorderRadius.circular(26),
                            ),
                            child: Icon(
                              Icons.school_outlined,
                              size: 46,
                              color: colors.onPrimary,
                            ),
                          ),
                          const SizedBox(height: 22),
                          Text(
                            'CampusMarket',
                            style: theme.textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Marketplace universitario',
                            style: theme.textTheme.bodyLarge?.copyWith(
                              color: colors.onSurfaceVariant,
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

          if (compacto) {
            return Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [contenido, visual],
            );
          }

          return Row(
            children: [
              Expanded(flex: 6, child: contenido),
              Expanded(flex: 4, child: visual),
            ],
          );
        },
      ),
    );
  }
}

class _Burbuja extends StatelessWidget {
  const _Burbuja({required this.size, required this.color});

  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(color: color, shape: BoxShape.circle),
    );
  }
}

class _BeneficiosInicio extends StatelessWidget {
  const _BeneficiosInicio();

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final ancho = constraints.maxWidth;
        final itemWidth = ancho >= 900
            ? (ancho - 36) / 3
            : ancho >= 560
            ? (ancho - 18) / 2
            : ancho;

        return Wrap(
          spacing: 18,
          runSpacing: 18,
          children: [
            _BeneficioCard(
              width: itemWidth,
              icono: Icons.storefront_outlined,
              titulo: 'Catálogo real',
              descripcion: 'Búsqueda y filtros sobre publicaciones persistidas.',
            ),
            _BeneficioCard(
              width: itemWidth,
              icono: Icons.photo_library_outlined,
              titulo: 'Productos con fotos',
              descripcion: 'Hasta tres imágenes por publicación y galería de detalle.',
            ),
            _BeneficioCard(
              width: itemWidth,
              icono: Icons.devices_outlined,
              titulo: 'Experiencia responsive',
              descripcion: 'Interfaz adaptada para escritorio, tablet y móvil.',
            ),
          ],
        );
      },
    );
  }
}

class _BeneficioCard extends StatelessWidget {
  const _BeneficioCard({
    required this.width,
    required this.icono,
    required this.titulo,
    required this.descripcion,
  });

  final double width;
  final IconData icono;
  final String titulo;
  final String descripcion;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return SizedBox(
      width: width,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: colors.primaryContainer,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Icon(icono, color: colors.primary),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      titulo,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      descripcion,
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: colors.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _HallazgoDestacado extends StatelessWidget {
  const _HallazgoDestacado({required this.publicacion, this.onTap});
  final PublicacionCatalogo publicacion;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) => ClipRRect(
    borderRadius: BorderRadius.circular(26),
    child: InkWell(
      onTap: onTap,
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        AspectRatio(
          aspectRatio: 16 / 10,
          child: Image.network(
            publicacion.imagenPrincipal!.imagenUrl, fit: BoxFit.cover,
            semanticLabel: publicacion.titulo,
            errorBuilder: (_, _, _) => const Center(child: Icon(Icons.inventory_2_outlined, size: 68)),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(22),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('UN HALLAZGO DE LA COMUNIDAD', style: TextStyle(fontSize: 11, letterSpacing: 1.4, fontWeight: FontWeight.w800, color: Theme.of(context).colorScheme.primary)),
            const SizedBox(height: 10),
            Text(publicacion.titulo, maxLines: 2, overflow: TextOverflow.ellipsis, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text(formatoPrecio(publicacion.precio), style: Theme.of(context).textTheme.titleMedium?.copyWith(color: Theme.of(context).colorScheme.primary)),
          ]),
        ),
      ]),
    ),
  );
}
