import 'package:flutter/material.dart';

import '../shared/api_error.dart';
import 'administracion_api.dart';

class ModeracionPage extends StatefulWidget {
  const ModeracionPage({super.key});
  @override
  State<ModeracionPage> createState() => _ModeracionPageState();
}

class _ModeracionPageState extends State<ModeracionPage> {
  final _api = AdministracionApi();
  List<Map<String, dynamic>> _reportes = [];
  bool _busy = true;
  String? _error;

  @override
  void initState() { super.initState(); _cargar(); }

  @override
  void dispose() { _api.dispose(); super.dispose(); }

  Future<void> _cargar() async {
    setState(() { _busy = true; _error = null; });
    try {
      final reports = await _api.pendientes();
      if (mounted) setState(() => _reportes = reports);
    } catch (error) {
      if (mounted) setState(() => _error = readableError(error));
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _revisar(Map<String, dynamic> reporte, String decision) async {
    final nota = await showDialog<String>(
      context: context, builder: (_) => _DecisionDialog(decision: decision),
    );
    if (nota == null) return;
    setState(() => _busy = true);
    try {
      await _api.resolver(reporte['id'] as int, decision, nota);
      await _cargar();
    } catch (error) {
      if (mounted) setState(() { _error = readableError(error); _busy = false; });
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text('Reportes de la comunidad'),
      actions: [IconButton(tooltip: 'Actualizar reportes', onPressed: _busy ? null : _cargar, icon: const Icon(Icons.refresh))],
    ),
    body: SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Center(child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 900),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text('Una comunidad que cuidamos juntos', style: Theme.of(context).textTheme.headlineMedium),
          const SizedBox(height: 12),
          const Text('Revisa los motivos y deja una nota con la decisión. Ocultar retira el producto del catálogo; su propietario conserva su gestión.'),
          const SizedBox(height: 24),
          if (_busy) const LinearProgressIndicator(),
          if (_error != null) ...[
            Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
            TextButton(onPressed: _busy ? null : _cargar, child: const Text('Reintentar')),
          ],
          if (!_busy && _error == null && _reportes.isEmpty)
            const Padding(
              padding: EdgeInsets.all(40),
              child: Column(children: [
                Icon(Icons.check_circle_outline, size: 60),
                SizedBox(height: 18),
                Text('No hay reportes pendientes.'),
              ]),
            ),
          for (final reporte in _reportes) ...[
            const SizedBox(height: 16),
            Card(child: Padding(
              padding: const EdgeInsets.all(22),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(reporte['titulo_publicacion']?.toString() ?? 'Publicación retirada', style: Theme.of(context).textTheme.titleLarge),
                const SizedBox(height: 12),
                Text(reporte['motivo'] as String),
                const SizedBox(height: 20),
                Wrap(spacing: 12, runSpacing: 12, children: [
                  FilledButton.icon(
                    onPressed: _busy ? null : () => _revisar(reporte, 'ocultado'),
                    icon: const Icon(Icons.visibility_off_outlined), label: const Text('Ocultar publicación'),
                  ),
                  OutlinedButton(
                    onPressed: _busy ? null : () => _revisar(reporte, 'descartado'),
                    child: const Text('Descartar reporte'),
                  ),
                ]),
              ]),
            )),
          ],
        ]),
      )),
    ),
  );
}

class _DecisionDialog extends StatefulWidget {
  const _DecisionDialog({required this.decision});
  final String decision;
  @override
  State<_DecisionDialog> createState() => _DecisionDialogState();
}

class _DecisionDialogState extends State<_DecisionDialog> {
  final _nota = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  @override
  void dispose() { _nota.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) => AlertDialog(
    scrollable: true,
    title: Text(widget.decision == 'ocultado' ? 'Ocultar publicación' : 'Descartar reporte'),
    content: SizedBox(
      width: 480,
      child: Form(key: _formKey, child: TextFormField(
        key: const Key('resolucion-nota'),
        controller: _nota, minLines: 2, maxLines: 4, maxLength: 500,
        decoration: const InputDecoration(labelText: 'Motivo de tu decisión'),
        validator: (value) => (value ?? '').trim().length < 5 ? 'Ingresa una nota de al menos 5 caracteres.' : null,
      )),
    ),
    actions: [
      TextButton(onPressed: () => Navigator.of(context).pop(), child: const Text('Cancelar')),
      FilledButton(onPressed: () {
        if (_formKey.currentState!.validate()) Navigator.of(context).pop(_nota.text.trim());
      }, child: const Text('Confirmar decisión')),
    ],
  );
}
