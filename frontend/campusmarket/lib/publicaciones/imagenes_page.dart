import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../shared/api_error.dart';
import 'publicaciones_api.dart';

class ImagenesPage extends StatefulWidget {
  const ImagenesPage({super.key, required this.publicacionId});
  final int publicacionId;
  @override
  State<ImagenesPage> createState() => _ImagenesPageState();
}

class _ImagenesPageState extends State<ImagenesPage> {
  final _api = PublicacionesApi();
  List<Map<String, dynamic>> _imagenes = [];
  String _titulo = '';
  bool _busy = true;
  String? _error;

  @override
  void initState() { super.initState(); _cargar(); }
  @override
  void dispose() { _api.dispose(); super.dispose(); }

  Future<void> _cargar() async {
    setState(() { _busy = true; _error = null; });
    try {
      final propias = await _api.listarMisPublicaciones();
      final publicacion = propias.where((item) => item['id'] == widget.publicacionId).firstOrNull;
      if (publicacion == null) throw const ApiException('Esta publicación ya no está disponible.');
      final imagenes = (publicacion['imagenes'] as List).cast<Map<String, dynamic>>();
      imagenes.sort((a, b) => (a['orden'] as int).compareTo(b['orden'] as int));
      if (!mounted) return;
      setState(() {
        _titulo = publicacion['titulo'] as String;
        _imagenes = imagenes;
      });
    } catch (error) {
      if (mounted) setState(() => _error = readableError(error));
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _accion(Future<void> Function() operation) async {
    if (_busy) return;
    setState(() { _busy = true; _error = null; });
    try {
      await operation();
      await _cargar();
    } catch (error) {
      if (mounted) setState(() => _error = readableError(error));
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _subir() async {
    await _accion(() async {
      final files = await FilePicker.pickFiles(
        type: FileType.custom, allowedExtensions: const ['jpg', 'jpeg', 'png', 'webp'],
      );
      if (files.isEmpty) return;
      final disponibles = 3 - _imagenes.length;
      if (files.length > disponibles) {
        throw ApiException('Puedes agregar hasta $disponibles fotografías más.');
      }
      final preparadas = <ImagenPublicacion>[];
      for (final file in files) {
        final length = file.lengthSync() ?? await file.length();
        if (length == null || length <= 0 || length > 5 * 1024 * 1024) {
          throw const ApiException('Cada fotografía debe tener contenido y pesar máximo 5 MB.');
        }
        final bytes = await file.readAsBytes();
        if (bytes.isEmpty || bytes.length > 5 * 1024 * 1024) {
          throw const ApiException('La fotografía está vacía o supera 5 MB.');
        }
        preparadas.add(ImagenPublicacion(nombre: file.name, bytes: bytes));
      }
      await _api.subirImagenes(publicacionId: widget.publicacionId, imagenes: preparadas);
    });
  }

  Future<void> _eliminar(Map<String, dynamic> imagen) async {
    final accepted = await showDialog<bool>(
      context: context, builder: (context) => AlertDialog(
        title: const Text('Eliminar fotografía'),
        content: const Text('La fotografía se retirará de esta publicación.'),
        actions: [
          TextButton(onPressed: () => Navigator.of(context).pop(false), child: const Text('Cancelar')),
          FilledButton(onPressed: () => Navigator.of(context).pop(true), child: const Text('Eliminar fotografía')),
        ],
      ),
    );
    if (accepted == true) {
      await _accion(() => _api.eliminarImagen(widget.publicacionId, imagen['id'] as int));
    }
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: const Text('Fotografías de tu publicación')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Center(child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1000),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text(_titulo, style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 12),
            const Text('Hasta 3 fotografías. La principal aparece en las tarjetas del catálogo. JPG, PNG o WebP, máximo 5 MB por imagen.'),
            const SizedBox(height: 24),
            if (_busy) const LinearProgressIndicator(),
            if (_error != null) ...[
              const SizedBox(height: 16),
              Text(_error!, style: TextStyle(color: colors.error)),
              TextButton(onPressed: _busy ? null : _cargar, child: const Text('Actualizar fotografías')),
            ],
            const SizedBox(height: 20),
            LayoutBuilder(builder: (context, constraints) {
              final width = constraints.maxWidth >= 760
                  ? (constraints.maxWidth - 32) / 3
                  : constraints.maxWidth >= 500 ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth;
              return Wrap(spacing: 16, runSpacing: 16, children: [
                for (final imagen in _imagenes)
                  SizedBox(width: width, child: Card(
                    clipBehavior: Clip.antiAlias,
                    child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                      AspectRatio(
                        aspectRatio: 4 / 3,
                        child: Image.network(
                          _api.baseUrl + (imagen['imagen_url'] as String),
                          fit: BoxFit.cover,
                          errorBuilder: (_, _, _) => const Center(child: Icon(Icons.broken_image_outlined, size: 48)),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(14),
                        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                          if (imagen['es_principal'] == true)
                            const Row(children: [Icon(Icons.star, size: 18), SizedBox(width: 6), Text('Fotografía principal')])
                          else
                            TextButton.icon(
                              key: Key("imagen-principal-${imagen['id']}"),
                              onPressed: _busy ? null : () => _accion(() => _api.elegirPrincipal(widget.publicacionId, imagen['id'] as int)),
                              icon: const Icon(Icons.star_outline), label: const Text('Elegir principal'),
                            ),
                          const SizedBox(height: 8),
                          TextButton.icon(
                            key: Key("imagen-eliminar-${imagen['id']}"),
                            onPressed: _busy ? null : () => _eliminar(imagen),
                            icon: const Icon(Icons.delete_outline), label: const Text('Eliminar fotografía'),
                          ),
                        ]),
                      ),
                    ]),
                  )),
              ]);
            }),
            if (!_busy && _imagenes.isEmpty)
              const Padding(
                padding: EdgeInsets.all(32),
                child: Column(children: [Icon(Icons.add_photo_alternate_outlined, size: 64), SizedBox(height: 16), Text('Tu producto merece una buena primera impresión.')]),
              ),
            const SizedBox(height: 24),
            FilledButton.icon(
              key: const Key('galeria-agregar'),
              onPressed: _busy || _imagenes.length >= 3 ? null : _subir,
              icon: const Icon(Icons.add_photo_alternate_outlined),
              label: Text(_imagenes.length >= 3 ? 'Tienes las 3 fotografías' : 'Agregar fotografías'),
            ),
          ]),
        )),
      ),
    );
  }
}
