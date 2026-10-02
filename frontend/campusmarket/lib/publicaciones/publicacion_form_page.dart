import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import 'publicaciones_api.dart';

class ImagenSeleccionada {
  const ImagenSeleccionada({required this.nombre, required this.bytes});

  final String nombre;
  final Uint8List bytes;

  int get size => bytes.length;
}

class PublicacionFormPage extends StatefulWidget {
  const PublicacionFormPage({super.key});

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
  bool _seleccionandoImagenes = false;

  @override
  void dispose() {
    _tituloController.dispose();
    _descripcionController.dispose();
    _precioController.dispose();
    super.dispose();
  }

  Future<void> _seleccionarImagenes() async {
    if (_guardando || _seleccionandoImagenes) {
      return;
    }

    final disponibles = _maxImagenes - _imagenes.length;

    if (disponibles <= 0) {
      _mostrarMensaje('Ya seleccionaste el máximo de $_maxImagenes imágenes.');
      return;
    }

    setState(() {
      _seleccionandoImagenes = true;
    });

    try {
      final archivos = await FilePicker.pickFiles(
        type: FileType.custom,
        allowedExtensions: const ['jpg', 'jpeg', 'png', 'webp'],
      );

      if (archivos.isEmpty) {
        return;
      }

      final nuevasImagenes = <ImagenSeleccionada>[];

      for (final archivo in archivos) {
        if (nuevasImagenes.length >= disponibles) {
          break;
        }

        final extension = archivo.name.split('.').last.toLowerCase();

        if (!const {'jpg', 'jpeg', 'png', 'webp'}.contains(extension)) {
          _mostrarMensaje('${archivo.name}: formato no permitido.');
          continue;
        }

        final longitud = archivo.lengthSync() ?? await archivo.length();

        if (longitud == null) {
          _mostrarMensaje(
            'No fue posible determinar el tamaño de ${archivo.name}.',
          );
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

      if (!mounted) {
        return;
      }

      if (nuevasImagenes.isNotEmpty) {
        setState(() {
          _imagenes.addAll(nuevasImagenes);
        });
      }

      if (archivos.length > disponibles) {
        _mostrarMensaje(
          'Solo se permiten $_maxImagenes imágenes por publicación.',
        );
      }
    } catch (_) {
      if (!mounted) {
        return;
      }

      _mostrarMensaje('No fue posible abrir el selector de imágenes.');
    } finally {
      if (mounted) {
        setState(() {
          _seleccionandoImagenes = false;
        });
      }
    }
  }

  void _eliminarImagen(int index) {
    if (_guardando) {
      return;
    }

    setState(() {
      _imagenes.removeAt(index);
    });
  }

  Future<void> _guardar() async {
    if (_guardando) {
      return;
    }

    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _guardando = true;
    });

    Map<String, dynamic>? creada;

    try {
      creada = await _api.crearPublicacion(
        titulo: _tituloController.text.trim(),
        descripcion: _descripcionController.text.trim(),
        precio: double.parse(_precioController.text.trim()),
        modalidad: _modalidad,
        estado: _estado,
      );

      final rawId = creada['id'];

      if (rawId is! num) {
        throw Exception('La API no devolvió un identificador válido.');
      }

      final publicacionId = rawId.toInt();

      if (_imagenes.isNotEmpty) {
        final imagenesApi = _imagenes
            .map(
              (imagen) =>
                  ImagenPublicacion(nombre: imagen.nombre, bytes: imagen.bytes),
            )
            .toList();

        await _api.subirImagenes(
          publicacionId: publicacionId,
          imagenes: imagenesApi,
        );
      }

      if (!mounted) {
        return;
      }

      final cantidadImagenes = _imagenes.length;

      _mostrarMensaje(
        cantidadImagenes == 0
            ? 'Publicación #$publicacionId guardada correctamente.'
            : 'Publicación #$publicacionId guardada con '
                  '$cantidadImagenes '
                  '${cantidadImagenes == 1 ? 'imagen' : 'imágenes'}.',
      );

      _limpiarFormulario();
    } on PublicacionTemporalmenteNoDisponible catch (error) {
      if (!mounted) {
        return;
      }

      _mostrarMensaje(error.mensaje);
    } catch (_) {
      if (!mounted) {
        return;
      }

      if (creada != null) {
        final publicacionId = creada['id'];

        _mostrarMensaje(
          'La publicación #$publicacionId fue creada, '
          'pero no fue posible subir todas las imágenes.',
        );
      } else {
        _mostrarMensaje('No fue posible guardar la publicación.');
      }
    } finally {
      if (mounted) {
        setState(() {
          _guardando = false;
        });
      }
    }
  }

  void _limpiarFormulario() {
    _tituloController.clear();
    _descripcionController.clear();
    _precioController.clear();

    setState(() {
      _imagenes.clear();
      _modalidad = 'venta';
      _estado = 'usado';
    });
  }

  void _mostrarMensaje(String mensaje) {
    if (!mounted) {
      return;
    }

    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(mensaje)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('CampusMarket · Nueva publicación')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 820),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Publicar un producto',
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.w800),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Completa la información y agrega '
                    'hasta $_maxImagenes fotografías del producto.',
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: 28),

                  _buildImagenesSection(),

                  const SizedBox(height: 28),

                  TextFormField(
                    controller: _tituloController,
                    enabled: !_guardando,
                    textInputAction: TextInputAction.next,
                    decoration: const InputDecoration(
                      labelText: 'Título',
                      hintText: 'Ej. Calculadora Casio FX-991',
                      prefixIcon: Icon(Icons.sell_outlined),
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      if (value == null || value.trim().length < 3) {
                        return 'Ingresa un título de al menos '
                            '3 caracteres.';
                      }

                      if (value.trim().length > 100) {
                        return 'El título no puede superar '
                            '100 caracteres.';
                      }

                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  TextFormField(
                    controller: _descripcionController,
                    enabled: !_guardando,
                    minLines: 4,
                    maxLines: 6,
                    decoration: const InputDecoration(
                      labelText: 'Descripción',
                      hintText: 'Describe el producto y su condición.',
                      prefixIcon: Icon(Icons.description_outlined),
                      border: OutlineInputBorder(),
                      alignLabelWithHint: true,
                    ),
                    validator: (value) {
                      if (value == null || value.trim().length < 3) {
                        return 'Ingresa una descripción.';
                      }

                      if (value.trim().length > 500) {
                        return 'La descripción no puede superar '
                            '500 caracteres.';
                      }

                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  TextFormField(
                    controller: _precioController,
                    enabled: !_guardando,
                    keyboardType: const TextInputType.numberWithOptions(
                      decimal: true,
                    ),
                    decoration: const InputDecoration(
                      labelText: 'Precio',
                      hintText: '85000',
                      prefixText: '\$ ',
                      prefixIcon: Icon(Icons.payments_outlined),
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      final parsed = double.tryParse(
                        (value ?? '').replaceAll(',', '.').trim(),
                      );

                      if (parsed == null || parsed <= 0) {
                        return 'Ingresa un precio mayor '
                            'que cero.';
                      }

                      return null;
                    },
                  ),

                  const SizedBox(height: 16),

                  LayoutBuilder(
                    builder: (context, constraints) {
                      final compact = constraints.maxWidth < 560;

                      final modalidad = DropdownButtonFormField<String>(
                        key: ValueKey('modalidad-$_modalidad'),
                        initialValue: _modalidad,
                        decoration: const InputDecoration(
                          labelText: 'Modalidad',
                          prefixIcon: Icon(Icons.swap_horiz),
                          border: OutlineInputBorder(),
                        ),
                        items: const [
                          DropdownMenuItem(
                            value: 'venta',
                            child: Text('Venta'),
                          ),
                          DropdownMenuItem(
                            value: 'alquiler',
                            child: Text('Alquiler'),
                          ),
                        ],
                        onChanged: _guardando
                            ? null
                            : (value) {
                                if (value == null) {
                                  return;
                                }

                                setState(() {
                                  _modalidad = value;
                                });
                              },
                      );

                      final estado = DropdownButtonFormField<String>(
                        key: ValueKey('estado-$_estado'),
                        initialValue: _estado,
                        decoration: const InputDecoration(
                          labelText: 'Estado',
                          prefixIcon: Icon(Icons.verified_outlined),
                          border: OutlineInputBorder(),
                        ),
                        items: const [
                          DropdownMenuItem(
                            value: 'nuevo',
                            child: Text('Nuevo'),
                          ),
                          DropdownMenuItem(
                            value: 'usado',
                            child: Text('Usado'),
                          ),
                          DropdownMenuItem(
                            value: 'reacondicionado',
                            child: Text('Reacondicionado'),
                          ),
                        ],
                        onChanged: _guardando
                            ? null
                            : (value) {
                                if (value == null) {
                                  return;
                                }

                                setState(() {
                                  _estado = value;
                                });
                              },
                      );

                      if (compact) {
                        return Column(
                          children: [
                            modalidad,
                            const SizedBox(height: 16),
                            estado,
                          ],
                        );
                      }

                      return Row(
                        children: [
                          Expanded(child: modalidad),
                          const SizedBox(width: 16),
                          Expanded(child: estado),
                        ],
                      );
                    },
                  ),

                  const SizedBox(height: 28),

                  SizedBox(
                    height: 54,
                    child: FilledButton.icon(
                      onPressed: _guardando ? null : _guardar,
                      icon: _guardando
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.publish_outlined),
                      label: Text(
                        _guardando ? 'Publicando...' : 'Publicar producto',
                      ),
                    ),
                  ),

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
          ),
        ),
      ),
    );
  }

  Widget _buildImagenesSection() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerLowest,
        border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
        borderRadius: BorderRadius.circular(20),
      ),
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
                  color: Theme.of(context).colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(
                  Icons.photo_library_outlined,
                  color: Theme.of(context).colorScheme.onPrimaryContainer,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Fotos del producto',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Hasta $_maxImagenes imágenes · '
                      'JPG, JPEG, PNG o WEBP · '
                      'máximo 5 MB cada una',
                      style: TextStyle(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 12),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 11,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
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
    );
  }

  Widget _buildEmptyImagesState() {
    return InkWell(
      onTap: _guardando || _seleccionandoImagenes ? null : _seleccionarImagenes,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 34, horizontal: 20),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: Theme.of(context).colorScheme.outlineVariant,
          ),
        ),
        child: Column(
          children: [
            Icon(
              Icons.add_photo_alternate_outlined,
              size: 46,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 12),
            Text(
              _seleccionandoImagenes
                  ? 'Abriendo selector...'
                  : 'Seleccionar fotografías',
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 5),
            Text(
              'La primera imagen será la principal',
              style: TextStyle(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
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
                    color: Theme.of(
                      context,
                    ).colorScheme.surfaceContainerHighest,
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
          border: Border.all(
            color: Theme.of(context).colorScheme.outlineVariant,
          ),
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
