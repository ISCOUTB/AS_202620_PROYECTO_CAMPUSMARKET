import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../shared/api_error.dart';
import 'publicaciones_api.dart';

class ImagenSeleccionada {
  const ImagenSeleccionada({required this.nombre, required this.bytes});

  final String nombre;
  final Uint8List bytes;

  int get size => bytes.length;
}

class PublicacionFormPage extends StatefulWidget {
  const PublicacionFormPage({super.key, this.onPublicada});

  final VoidCallback? onPublicada;

  @override
  State<PublicacionFormPage> createState() => _PublicacionFormPageState();
}

class _PublicacionFormPageState extends State<PublicacionFormPage> {
  static const int _maxImagenes = 3;
  static const int _maxImageBytes = 5 * 1024 * 1024;

  final _formKey = GlobalKey<FormState>();
  final _tituloController = TextEditingController();
  final _descripcionController = TextEditingController();
  final _precioController = TextEditingController();
  final _api = PublicacionesApi();
  final List<ImagenSeleccionada> _imagenes = [];

  String _modalidad = 'venta';
  String _estado = 'usado';
  bool _guardando = false;
  int? _publicacionPendiente;
  int _imagenesSubidas = 0;
  String? _errorGuardado;
  bool _seleccionandoImagenes = false;

  @override
  void dispose() {
    _tituloController.dispose();
    _descripcionController.dispose();
    _precioController.dispose();
    super.dispose();
  }

  Future<void> _seleccionarImagenes() async {
    if (_guardando || _seleccionandoImagenes) return;

    if (_publicacionPendiente != null) return;
    final disponibles = _maxImagenes - _imagenes.length;
    if (disponibles <= 0) {
      _mostrarMensaje('Ya seleccionaste el máximo de $_maxImagenes imágenes.');
      return;
    }

    setState(() => _seleccionandoImagenes = true);

    try {
      final archivos = await FilePicker.pickFiles(
        type: FileType.custom,
        allowedExtensions: const ['jpg', 'jpeg', 'png', 'webp'],
      );

      if (archivos.isEmpty) return;

      final nuevasImagenes = <ImagenSeleccionada>[];

      for (final archivo in archivos) {
        if (nuevasImagenes.length >= disponibles) break;

        final extension = archivo.name.split('.').last.toLowerCase();
        if (!const {'jpg', 'jpeg', 'png', 'webp'}.contains(extension)) {
          _mostrarMensaje('${archivo.name}: formato no permitido.');
          continue;
        }

        final longitud = archivo.lengthSync() ?? await archivo.length();
        if (longitud == null) {
          _mostrarMensaje('No fue posible determinar el tamaño de ${archivo.name}.');
          continue;
        }
        if (longitud > _maxImageBytes) {
          _mostrarMensaje('${archivo.name} supera el máximo de 5 MB.');
          continue;
        }

        try {
          final bytes = await archivo.readAsBytes();
          if (bytes.isEmpty) {
            _mostrarMensaje('${archivo.name} está vacío.');
            continue;
          }
          if (bytes.length > _maxImageBytes) {
            _mostrarMensaje('${archivo.name} supera el máximo de 5 MB.');
            continue;
          }
          nuevasImagenes.add(
            ImagenSeleccionada(nombre: archivo.name, bytes: bytes),
          );
        } catch (_) {
          _mostrarMensaje('No fue posible leer ${archivo.name}.');
        }
      }

      if (!mounted) return;

      if (nuevasImagenes.isNotEmpty) {
        setState(() => _imagenes.addAll(nuevasImagenes));
      }

      if (archivos.length > disponibles) {
        _mostrarMensaje('Solo se permiten $_maxImagenes imágenes por publicación.');
      }
    } catch (_) {
      if (mounted) {
        _mostrarMensaje('No fue posible abrir el selector de imágenes.');
      }
    } finally {
      if (mounted) setState(() => _seleccionandoImagenes = false);
    }
  }

  void _eliminarImagen(int index) {
    if (_guardando || _publicacionPendiente != null) return;
    setState(() => _imagenes.removeAt(index));
  }

  Future<void> _guardar() async {
    if (_guardando || !_formKey.currentState!.validate()) return;
    FocusScope.of(context).unfocus();
    setState(() { _guardando = true; _errorGuardado = null; });
    try {
      if (_publicacionPendiente == null) {
        final creada = await _api.crearPublicacion(
          titulo: _tituloController.text.trim(),
          descripcion: _descripcionController.text.trim(),
          precio: double.parse(_precioController.text.trim().replaceAll(',', '.')),
          modalidad: _modalidad, estado: _estado,
        );
        _publicacionPendiente = (creada['id'] as num).toInt();
      }
      final id = _publicacionPendiente!;
      while (_imagenesSubidas < _imagenes.length) {
        final imagen = _imagenes[_imagenesSubidas];
        await _api.subirImagen(
          publicacionId: id, imagen: ImagenPublicacion(nombre: imagen.nombre, bytes: imagen.bytes),
        );
        _imagenesSubidas++;
      }
      if (!mounted) return;
      _mostrarMensaje('Tu publicación ya está en CampusMarket.');
      _limpiarFormulario();
      widget.onPublicada?.call();
    } catch (error) {
      if (!mounted) return;
      setState(() => _errorGuardado = _publicacionPendiente == null
        ? readableError(error)
        : 'Tu publicación ya fue creada. Reintenta para subir las imágenes pendientes. ${readableError(error)}');
    } finally {
      if (mounted) setState(() => _guardando = false);
    }
  }

  void _limpiarFormulario() {
    _tituloController.clear();
    _descripcionController.clear();
    _precioController.clear();
    setState(() {
      _imagenes.clear();
      _publicacionPendiente = null;
      _imagenesSubidas = 0;
      _errorGuardado = null;
      _modalidad = 'venta';
      _estado = 'usado';
    });
  }

  void _mostrarMensaje(String mensaje) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(mensaje)));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 28, 24, 48),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1320),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Publicar producto',
                      style: theme.textTheme.displaySmall?.copyWith(
                        fontWeight: FontWeight.w900,
                        height: 1.05,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      'Comparte con la comunidad universitaria. Completa la información del producto y agrega hasta $_maxImagenes fotografías.',
                      style: theme.textTheme.bodyLarge?.copyWith(
                        color: colors.onSurfaceVariant,
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 28),
                    LayoutBuilder(
                      builder: (context, constraints) {
                        final desktop = constraints.maxWidth >= 1000;

                        final fotos = Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            _buildImagenesSection(),
                            const SizedBox(height: 18),
                            _buildConsejos(),
                          ],
                        );

                        final formulario = _buildFormularioCard();

                        if (!desktop) {
                          return Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              fotos,
                              const SizedBox(height: 24),
                              formulario,
                            ],
                          );
                        }

                        return Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(flex: 5, child: fotos),
                            const SizedBox(width: 24),
                            Expanded(flex: 6, child: formulario),
                          ],
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFormularioCard() {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: colors.primaryContainer,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(Icons.description_outlined, color: colors.primary),
                ),
                const SizedBox(width: 12),
                Text(
                  'Información del producto',
                  style: theme.textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            TextFormField(
              key: const Key('publicacion-titulo'),
              controller: _tituloController,
              enabled: !_guardando && _publicacionPendiente == null,
              textInputAction: TextInputAction.next,
              decoration: const InputDecoration(
                labelText: 'Título',
                hintText: 'Ej. Calculadora Casio FX-991',
                prefixIcon: Icon(Icons.sell_outlined),
              ),
              validator: (value) {
                if (value == null || value.trim().length < 3) {
                  return 'Ingresa un título de al menos 3 caracteres.';
                }
                if (value.trim().length > 100) {
                  return 'El título no puede superar 100 caracteres.';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            LayoutBuilder(
              builder: (context, constraints) {
                final compact = constraints.maxWidth < 620;
                final precio = TextFormField(
                  key: const Key('publicacion-precio'),
                  controller: _precioController,
                  enabled: !_guardando && _publicacionPendiente == null,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(
                    labelText: 'Precio',
                    hintText: '85000',
                    prefixText: '\$ ',
                    prefixIcon: Icon(Icons.payments_outlined),
                  ),
                  validator: (value) {
                    final parsed = double.tryParse(
                      (value ?? '').replaceAll(',', '.').trim(),
                    );
                    if (parsed == null || !parsed.isFinite || parsed <= 0 || parsed > 9999999999.99 || ((parsed * 100) - (parsed * 100).round()).abs() > 0.0001) {
                      return 'Usa un precio positivo con máximo 2 decimales.';
                    }
                    return null;
                  },
                );

                final modalidad = DropdownButtonFormField<String>(
                  key: ValueKey('modalidad-$_modalidad'),
                  initialValue: _modalidad,
                  decoration: const InputDecoration(
                    labelText: 'Modalidad',
                    prefixIcon: Icon(Icons.swap_horiz),
                  ),
                  items: const [
                    DropdownMenuItem(value: 'venta', child: Text('Venta')),
                    DropdownMenuItem(value: 'alquiler', child: Text('Alquiler')),
                  ],
                  onChanged: _guardando || _publicacionPendiente != null
                      ? null
                      : (value) {
                          if (value != null) setState(() => _modalidad = value);
                        },
                );

                if (compact) {
                  return Column(
                    children: [precio, const SizedBox(height: 16), modalidad],
                  );
                }

                return Row(
                  children: [
                    Expanded(child: precio),
                    const SizedBox(width: 16),
                    Expanded(child: modalidad),
                  ],
                );
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              key: ValueKey('estado-$_estado'),
              initialValue: _estado,
              decoration: const InputDecoration(
                labelText: 'Estado del producto',
                prefixIcon: Icon(Icons.verified_outlined),
              ),
              items: const [
                DropdownMenuItem(value: 'nuevo', child: Text('Nuevo')),
                DropdownMenuItem(value: 'usado', child: Text('Usado')),
                DropdownMenuItem(
                  value: 'reacondicionado',
                  child: Text('Reacondicionado'),
                ),
              ],
              onChanged: _guardando || _publicacionPendiente != null
                  ? null
                  : (value) {
                      if (value != null) setState(() => _estado = value);
                    },
            ),
            const SizedBox(height: 16),
            TextFormField(
              key: const Key('publicacion-descripcion'),
              controller: _descripcionController,
              enabled: !_guardando && _publicacionPendiente == null,
              minLines: 5,
              maxLines: 8,
              decoration: const InputDecoration(
                labelText: 'Descripción',
                hintText: 'Describe el producto y su condición.',
                prefixIcon: Icon(Icons.notes_outlined),
                alignLabelWithHint: true,
              ),
              validator: (value) {
                if (value == null || value.trim().length < 3) {
                  return 'Ingresa una descripción.';
                }
                if (value.trim().length > 500) {
                  return 'La descripción no puede superar 500 caracteres.';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 54,
              child: FilledButton.icon(
                key: const Key('publicacion-guardar'),
                onPressed: _guardando ? null : _guardar,
                icon: _guardando
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.send_outlined),
                label: Text(_guardando ? 'Publicando...' : _publicacionPendiente != null ? 'Reintentar imágenes' : 'Publicar producto'),
              ),
            ),
            if (_errorGuardado != null) ...[
              const SizedBox(height: 16),
              Semantics(liveRegion: true, child: Text(_errorGuardado!, style: TextStyle(color: colors.error))),
            ],
            if (_guardando) ...[
              const SizedBox(height: 12),
              const Text(
                'Guardando publicación y subiendo imágenes...',
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildConsejos() {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: colors.primaryContainer.withValues(alpha: 0.35),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: colors.outlineVariant),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.lightbulb_outline, color: colors.primary),
              const SizedBox(width: 8),
              Text(
                'Consejos para una mejor publicación',
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          const Text('• Usa fotos claras y representativas del producto.'),
          const SizedBox(height: 6),
          const Text('• Describe el estado de forma precisa.'),
          const SizedBox(height: 6),
          const Text('• Verifica el precio antes de publicar.'),
        ],
      ),
    );
  }

  Widget _buildImagenesSection() {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 46,
                  height: 46,
                  decoration: BoxDecoration(
                    color: colors.primaryContainer,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(Icons.photo_library_outlined, color: colors.primary),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Fotos del producto',
                        style: theme.textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Hasta $_maxImagenes imágenes · JPG, JPEG, PNG o WEBP · máximo 5 MB cada una',
                        style: TextStyle(color: colors.onSurfaceVariant),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 12),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 6),
                  decoration: BoxDecoration(
                    color: colors.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${_imagenes.length}/$_maxImagenes',
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            if (_imagenes.isEmpty)
              _buildEmptyImagesState()
            else
              Wrap(
                spacing: 14,
                runSpacing: 14,
                children: [
                  for (var index = 0; index < _imagenes.length; index++)
                    _buildImagenPreview(_imagenes[index], index),
                  if (_imagenes.length < _maxImagenes) _buildAgregarImagen(),
                ],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyImagesState() {
    final colors = Theme.of(context).colorScheme;

    return InkWell(
      onTap: _guardando || _seleccionandoImagenes ? null : _seleccionarImagenes,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: double.infinity,
        constraints: const BoxConstraints(minHeight: 260),
        padding: const EdgeInsets.symmetric(vertical: 34, horizontal: 20),
        decoration: BoxDecoration(
          color: colors.surfaceContainerLowest,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: colors.outlineVariant),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.add_photo_alternate_outlined, size: 52, color: colors.primary),
            const SizedBox(height: 12),
            Text(
              _seleccionandoImagenes ? 'Abriendo selector...' : 'Seleccionar fotografías',
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 5),
            Text(
              'La primera imagen será la principal',
              style: TextStyle(color: colors.onSurfaceVariant),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildImagenPreview(ImagenSeleccionada imagen, int index) {
    return SizedBox(
      width: 190,
      height: 160,
      child: Stack(
        children: [
          Positioned.fill(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.memory(
                imagen.bytes,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    color: Theme.of(context).colorScheme.surfaceContainerHighest,
                    alignment: Alignment.center,
                    child: const Icon(Icons.broken_image_outlined, size: 44),
                  );
                },
              ),
            ),
          ),
          Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: Theme.of(context).colorScheme.outlineVariant,
                ),
              ),
            ),
          ),
          Positioned(
            left: 8,
            top: 8,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 5),
              decoration: BoxDecoration(
                color: Colors.black.withValues(alpha: 0.65),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                index == 0 ? 'Principal' : 'Foto ${index + 1}',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          Positioned(
            right: 8,
            top: 8,
            child: Material(
              color: Colors.black.withValues(alpha: 0.65),
              shape: const CircleBorder(),
              child: InkWell(
                customBorder: const CircleBorder(),
                onTap: _guardando ? null : () => _eliminarImagen(index),
                child: const Padding(
                  padding: EdgeInsets.all(7),
                  child: Icon(Icons.close, color: Colors.white, size: 18),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAgregarImagen() {
    return InkWell(
      onTap: _guardando || _seleccionandoImagenes ? null : _seleccionarImagenes,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: 190,
        height: 160,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              _seleccionandoImagenes
                  ? Icons.hourglass_top
                  : Icons.add_photo_alternate_outlined,
              size: 38,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 10),
            Text(
              _seleccionandoImagenes ? 'Abriendo...' : 'Agregar fotos',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
    );
  }
}
