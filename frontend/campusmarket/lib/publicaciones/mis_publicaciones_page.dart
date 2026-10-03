import 'package:flutter/material.dart';

import 'publicaciones_api.dart';

class MisPublicacionesPage extends StatefulWidget {
  const MisPublicacionesPage({super.key, this.onChanged});

  final VoidCallback? onChanged;

  @override
  State<MisPublicacionesPage> createState() => _MisPublicacionesPageState();
}

class _MisPublicacionesPageState extends State<MisPublicacionesPage> {
  final PublicacionesApi _api = PublicacionesApi();
  String _filtro = 'todas';
  bool _cargando = true;
  String? _error;
  List<Map<String, dynamic>> _publicaciones = [];

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
      final publicaciones = await _api.listarMisPublicaciones();
      if (!mounted) return;
      setState(() => _publicaciones = publicaciones);
    } catch (error) {
      if (!mounted) return;
      setState(() => _error = error.toString());
    } finally {
      if (mounted) setState(() => _cargando = false);
    }
  }

  List<Map<String, dynamic>> get _filtradas {
    if (_filtro == 'todas') return _publicaciones;
    return _publicaciones
        .where((p) => p['estado_publicacion']?.toString() == _filtro)
        .toList();
  }

  int _contar(String estado) => _publicaciones
      .where((p) => p['estado_publicacion']?.toString() == estado)
      .length;

  Future<void> _cambiarEstado(
    Map<String, dynamic> publicacion,
    String estado,
  ) async {
    try {
      await _api.cambiarEstadoPublicacion(
        publicacionId: publicacion['id'] as int,
        estadoPublicacion: estado,
      );
      await _cargar();
      if (!mounted) return;
      widget.onChanged?.call();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Estado actualizado correctamente.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    }
  }

  Future<void> _eliminar(Map<String, dynamic> publicacion) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Eliminar publicación'),
        content: Text(
          '¿Deseas eliminar “${publicacion['titulo']}”? Esta acción no se puede deshacer.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          FilledButton.tonal(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );

    if (confirmar != true) return;

    try {
      await _api.eliminarPublicacion(publicacion['id'] as int);
      await _cargar();
      if (!mounted) return;
      widget.onChanged?.call();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Publicación eliminada.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    }
  }

  Future<void> _editar(Map<String, dynamic> publicacion) async {
    final resultado = await showDialog<Map<String, dynamic>>(
      context: context,
      builder: (context) => _EditarPublicacionDialog(publicacion: publicacion),
    );

    if (resultado == null) return;

    try {
      await _api.editarPublicacion(
        publicacionId: publicacion['id'] as int,
        titulo: resultado['titulo'] as String,
        descripcion: resultado['descripcion'] as String,
        precio: resultado['precio'] as double,
        modalidad: resultado['modalidad'] as String,
        estado: resultado['estado'] as String,
      );
      await _cargar();
      if (!mounted) return;
      widget.onChanged?.call();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Publicación actualizada.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString())),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return RefreshIndicator(
      onRefresh: _cargar,
      child: CustomScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        slivers: [
          SliverToBoxAdapter(
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.fromLTRB(24, 30, 24, 24),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    colors.primaryContainer.withValues(alpha: 0.55),
                    colors.surface,
                  ],
                ),
              ),
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 1180),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Mis publicaciones',
                        style: theme.textTheme.headlineMedium?.copyWith(
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Administra tus productos, disponibilidad y datos publicados.',
                        style: theme.textTheme.bodyLarge?.copyWith(
                          color: colors.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(height: 22),
                      Wrap(
                        spacing: 12,
                        runSpacing: 12,
                        children: [
                          _MetricCard(label: 'Total', value: _publicaciones.length),
                          _MetricCard(
                            label: 'Disponibles',
                            value: _contar('disponible'),
                          ),
                          _MetricCard(
                            label: 'Reservadas',
                            value: _contar('reservado'),
                          ),
                          _MetricCard(
                            label: 'Vendidas',
                            value: _contar('vendido'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1180),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(24, 22, 24, 14),
                  child: Wrap(
                    spacing: 10,
                    runSpacing: 10,
                    children: [
                      _FiltroChip(
                        label: 'Todas',
                        selected: _filtro == 'todas',
                        onTap: () => setState(() => _filtro = 'todas'),
                      ),
                      _FiltroChip(
                        label: 'Disponibles',
                        selected: _filtro == 'disponible',
                        onTap: () => setState(() => _filtro = 'disponible'),
                      ),
                      _FiltroChip(
                        label: 'Reservadas',
                        selected: _filtro == 'reservado',
                        onTap: () => setState(() => _filtro = 'reservado'),
                      ),
                      _FiltroChip(
                        label: 'Vendidas',
                        selected: _filtro == 'vendido',
                        onTap: () => setState(() => _filtro = 'vendido'),
                      ),
                      IconButton.filledTonal(
                        tooltip: 'Actualizar',
                        onPressed: _cargar,
                        icon: const Icon(Icons.refresh),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          if (_cargando)
            const SliverFillRemaining(
              hasScrollBody: false,
              child: Center(child: CircularProgressIndicator()),
            )
          else if (_error != null)
            SliverFillRemaining(
              hasScrollBody: false,
              child: _EstadoVacio(
                icon: Icons.cloud_off_outlined,
                title: 'No pudimos cargar tus publicaciones',
                message: _error!,
                onRetry: _cargar,
              ),
            )
          else if (_filtradas.isEmpty)
            SliverFillRemaining(
              hasScrollBody: false,
              child: _EstadoVacio(
                icon: Icons.inventory_2_outlined,
                title: 'No hay publicaciones en este estado',
                message: 'Cambia el filtro o crea una nueva publicación.',
                onRetry: _cargar,
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(24, 4, 24, 40),
              sliver: SliverList.separated(
                itemCount: _filtradas.length,
                separatorBuilder: (_, _) => const SizedBox(height: 14),
                itemBuilder: (context, index) {
                  final publicacion = _filtradas[index];
                  return Center(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 1180),
                      child: _PublicacionGestionCard(
                        publicacion: publicacion,
                        apiBaseUrl: _api.baseUrl,
                        onEditar: () => _editar(publicacion),
                        onEliminar: () => _eliminar(publicacion),
                        onCambiarEstado: (estado) =>
                            _cambiarEstado(publicacion, estado),
                      ),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({required this.label, required this.value});

  final String label;
  final int value;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Container(
      constraints: const BoxConstraints(minWidth: 135),
      padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
      decoration: BoxDecoration(
        color: colors.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: colors.outlineVariant),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '$value',
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.w900,
            ),
          ),
          Text(label, style: TextStyle(color: colors.onSurfaceVariant)),
        ],
      ),
    );
  }
}

class _FiltroChip extends StatelessWidget {
  const _FiltroChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => FilterChip(
    label: Text(label),
    selected: selected,
    onSelected: (_) => onTap(),
  );
}

class _PublicacionGestionCard extends StatelessWidget {
  const _PublicacionGestionCard({
    required this.publicacion,
    required this.apiBaseUrl,
    required this.onEditar,
    required this.onEliminar,
    required this.onCambiarEstado,
  });

  final Map<String, dynamic> publicacion;
  final String apiBaseUrl;
  final VoidCallback onEditar;
  final VoidCallback onEliminar;
  final ValueChanged<String> onCambiarEstado;

  String? _imagenPrincipalUrl() {
    final imagenes = publicacion['imagenes'];
    if (imagenes is! List || imagenes.isEmpty) return null;

    Map<String, dynamic>? principal;
    for (final item in imagenes) {
      if (item is Map<String, dynamic> && item['es_principal'] == true) {
        principal = item;
        break;
      }
    }

    principal ??= imagenes.first is Map<String, dynamic>
        ? imagenes.first as Map<String, dynamic>
        : null;

    final raw = principal?['imagen_url']?.toString();
    if (raw == null || raw.isEmpty) return null;
    if (raw.startsWith('http://') || raw.startsWith('https://')) return raw;
    return '$apiBaseUrl$raw';
  }

  String _formatearPrecio(double value) {
    final digits = value.round().toString();
    final buffer = StringBuffer();
    for (var i = 0; i < digits.length; i++) {
      if (i > 0 && (digits.length - i) % 3 == 0) {
        buffer.write('.');
      }
      buffer.write(digits[i]);
    }
    return 'COP \$${buffer.toString()}';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;
    final estadoPublicacion =
        publicacion['estado_publicacion']?.toString() ?? 'disponible';
    final precio = (publicacion['precio'] as num?)?.toDouble() ?? 0;
    final imagenUrl = _imagenPrincipalUrl();

    Widget fallbackVisual() => Center(
      child: Icon(
        Icons.inventory_2_outlined,
        size: 54,
        color: colors.secondary,
      ),
    );

    return Card(
      clipBehavior: Clip.antiAlias,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final compact = constraints.maxWidth < 720;
          final productVisual = Container(
            width: compact ? double.infinity : 160,
            height: compact ? 170 : 150,
            clipBehavior: Clip.antiAlias,
            decoration: BoxDecoration(
              color: colors.secondaryContainer.withValues(alpha: 0.55),
              borderRadius: BorderRadius.circular(14),
            ),
            child: imagenUrl == null
                ? fallbackVisual()
                : Image.network(
                    imagenUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (_, _, _) => fallbackVisual(),
                  ),
          );

          final details = Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    _EstadoBadge(estado: estadoPublicacion),
                    Chip(
                      label: Text(publicacion['estado']?.toString() ?? ''),
                      visualDensity: VisualDensity.compact,
                    ),
                    Chip(
                      label: Text(publicacion['modalidad']?.toString() ?? ''),
                      visualDensity: VisualDensity.compact,
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  publicacion['titulo']?.toString() ?? 'Publicación',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: theme.textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  publicacion['descripcion']?.toString() ?? '',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: colors.onSurfaceVariant),
                ),
                const SizedBox(height: 12),
                Text(
                  _formatearPrecio(precio),
                  style: theme.textTheme.titleLarge?.copyWith(
                    color: colors.primary,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 14),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    OutlinedButton.icon(
                      onPressed: onEditar,
                      icon: const Icon(Icons.edit_outlined),
                      label: const Text('Editar'),
                    ),
                    PopupMenuButton<String>(
                      onSelected: onCambiarEstado,
                      itemBuilder: (context) => const [
                        PopupMenuItem(
                          value: 'disponible',
                          child: Text('Marcar disponible'),
                        ),
                        PopupMenuItem(
                          value: 'reservado',
                          child: Text('Marcar reservado'),
                        ),
                        PopupMenuItem(
                          value: 'vendido',
                          child: Text('Marcar vendido'),
                        ),
                      ],
                      child: const _MenuEstadoButton(),
                    ),
                    TextButton.icon(
                      onPressed: onEliminar,
                      icon: const Icon(Icons.delete_outline),
                      label: const Text('Eliminar'),
                    ),
                  ],
                ),
              ],
            ),
          );

          return Padding(
            padding: const EdgeInsets.all(16),
            child: compact
                ? Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      productVisual,
                      const SizedBox(height: 16),
                      Row(children: [details]),
                    ],
                  )
                : Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      productVisual,
                      const SizedBox(width: 20),
                      details,
                    ],
                  ),
          );
        },
      ),
    );
  }
}

class _MenuEstadoButton extends StatelessWidget {
  const _MenuEstadoButton();

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
    decoration: BoxDecoration(
      border: Border.all(color: Theme.of(context).colorScheme.outline),
      borderRadius: BorderRadius.circular(12),
    ),
    child: const Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(Icons.swap_horiz, size: 18),
        SizedBox(width: 8),
        Text('Cambiar estado'),
        SizedBox(width: 4),
        Icon(Icons.arrow_drop_down),
      ],
    ),
  );
}

class _EstadoBadge extends StatelessWidget {
  const _EstadoBadge({required this.estado});

  final String estado;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final icon = switch (estado) {
      'vendido' => Icons.check_circle_outline,
      'reservado' => Icons.schedule_outlined,
      _ => Icons.storefront_outlined,
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: colors.primaryContainer,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: colors.primary),
          const SizedBox(width: 6),
          Text(
            estado[0].toUpperCase() + estado.substring(1),
            style: TextStyle(
              color: colors.onPrimaryContainer,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}

class _EstadoVacio extends StatelessWidget {
  const _EstadoVacio({
    required this.icon,
    required this.title,
    required this.message,
    required this.onRetry,
  });

  final IconData icon;
  final String title;
  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Center(
    child: Padding(
      padding: const EdgeInsets.all(32),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 480),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 58),
            const SizedBox(height: 16),
            Text(
              title,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 8),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 18),
            OutlinedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Actualizar'),
            ),
          ],
        ),
      ),
    ),
  );
}

class _EditarPublicacionDialog extends StatefulWidget {
  const _EditarPublicacionDialog({required this.publicacion});

  final Map<String, dynamic> publicacion;

  @override
  State<_EditarPublicacionDialog> createState() =>
      _EditarPublicacionDialogState();
}

class _EditarPublicacionDialogState extends State<_EditarPublicacionDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _titulo;
  late final TextEditingController _descripcion;
  late final TextEditingController _precio;
  late String _modalidad;
  late String _estado;

  @override
  void initState() {
    super.initState();
    _titulo = TextEditingController(text: widget.publicacion['titulo']?.toString());
    _descripcion = TextEditingController(
      text: widget.publicacion['descripcion']?.toString(),
    );
    _precio = TextEditingController(
      text: (widget.publicacion['precio'] as num?)?.toString() ?? '',
    );
    _modalidad = widget.publicacion['modalidad']?.toString() ?? 'venta';
    _estado = widget.publicacion['estado']?.toString() ?? 'usado';
  }

  @override
  void dispose() {
    _titulo.dispose();
    _descripcion.dispose();
    _precio.dispose();
    super.dispose();
  }

  void _guardar() {
    if (!_formKey.currentState!.validate()) return;
    Navigator.pop(context, {
      'titulo': _titulo.text.trim(),
      'descripcion': _descripcion.text.trim(),
      'precio': double.parse(_precio.text.trim()),
      'modalidad': _modalidad,
      'estado': _estado,
    });
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: const Text('Editar publicación'),
    content: SizedBox(
      width: 520,
      child: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _titulo,
                decoration: const InputDecoration(labelText: 'Título'),
                validator: (value) => value == null || value.trim().length < 3
                    ? 'Ingresa un título válido.'
                    : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _descripcion,
                minLines: 3,
                maxLines: 5,
                decoration: const InputDecoration(labelText: 'Descripción'),
                validator: (value) => value == null || value.trim().length < 3
                    ? 'Ingresa una descripción válida.'
                    : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _precio,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: const InputDecoration(labelText: 'Precio'),
                validator: (value) {
                  final parsed = double.tryParse(value?.trim() ?? '');
                  return parsed == null || parsed <= 0
                      ? 'Ingresa un precio válido.'
                      : null;
                },
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: _modalidad,
                decoration: const InputDecoration(labelText: 'Modalidad'),
                items: const [
                  DropdownMenuItem(value: 'venta', child: Text('Venta')),
                  DropdownMenuItem(value: 'alquiler', child: Text('Alquiler')),
                ],
                onChanged: (value) => setState(() => _modalidad = value ?? 'venta'),
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: _estado,
                decoration: const InputDecoration(labelText: 'Condición'),
                items: const [
                  DropdownMenuItem(value: 'nuevo', child: Text('Nuevo')),
                  DropdownMenuItem(value: 'usado', child: Text('Usado')),
                  DropdownMenuItem(
                    value: 'reacondicionado',
                    child: Text('Reacondicionado'),
                  ),
                ],
                onChanged: (value) => setState(() => _estado = value ?? 'usado'),
              ),
            ],
          ),
        ),
      ),
    ),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: const Text('Cancelar'),
      ),
      FilledButton.icon(
        onPressed: _guardar,
        icon: const Icon(Icons.save_outlined),
        label: const Text('Guardar cambios'),
      ),
    ],
  );
}
