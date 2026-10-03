import 'package:flutter/material.dart';

import '../shared/api_error.dart';
import '../usuarios/auth_page.dart';
import '../usuarios/session_controller.dart';
import 'administracion_api.dart';

class ReportarPublicacionButton extends StatelessWidget {
  const ReportarPublicacionButton({super.key, required this.publicacionId, this.propietarioId});
  final int publicacionId;
  final int? propietarioId;

  Future<void> _reportar(BuildContext context) async {
    final session = SessionController.instance;
    if (!session.authenticated) {
      final entered = await Navigator.of(context).push<bool>(MaterialPageRoute(builder: (_) => const AuthPage()));
      if (!context.mounted || entered != true || !session.authenticated) return;
    }
    if (session.usuario?.id == propietarioId) return;
    if (!context.mounted) return;
    final reported = await showDialog<bool>(
      context: context, builder: (_) => _ReporteDialog(publicacionId: publicacionId),
    );
    if (reported == true && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Reporte recibido. Gracias por cuidar la comunidad.')));
    }
  }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: SessionController.instance,
    builder: (context, _) {
      if (SessionController.instance.usuario?.id == propietarioId && propietarioId != null) {
        return const Text('Esta es tu publicación. Puedes gestionarla en Mis publicaciones.');
      }
      return OutlinedButton.icon(
        key: const Key('reportar-publicacion'),
        onPressed: () => _reportar(context),
        icon: const Icon(Icons.flag_outlined),
        label: const Text('Reportar publicación'),
      );
    },
  );
}

class _ReporteDialog extends StatefulWidget {
  const _ReporteDialog({required this.publicacionId});
  final int publicacionId;
  @override
  State<_ReporteDialog> createState() => _ReporteDialogState();
}

class _ReporteDialogState extends State<_ReporteDialog> {
  final _formKey = GlobalKey<FormState>();
  final _motivo = TextEditingController();
  final _api = AdministracionApi();
  bool _busy = false;
  String? _error;

  @override
  void dispose() {
    _motivo.dispose();
    _api.dispose();
    super.dispose();
  }

  Future<void> _enviar() async {
    if (_busy || !_formKey.currentState!.validate()) return;
    setState(() { _busy = true; _error = null; });
    try {
      await _api.reportar(widget.publicacionId, _motivo.text.trim());
      if (mounted) Navigator.of(context).pop(true);
    } catch (error) {
      if (mounted) setState(() => _error = readableError(error));
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    scrollable: true,
    title: const Text('Reportar publicación'),
    content: SizedBox(
      width: 480,
      child: Form(
        key: _formKey,
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Cuéntanos qué ocurre: contenido engañoso, un artículo inapropiado u otro problema.'),
          const SizedBox(height: 20),
          TextFormField(
            key: const Key('reporte-motivo'),
            controller: _motivo, enabled: !_busy, minLines: 3, maxLines: 5, maxLength: 500,
            decoration: const InputDecoration(labelText: 'Motivo del reporte'),
            validator: (value) => (value ?? '').trim().length < 10 ? 'Describe el problema con al menos 10 caracteres.' : null,
          ),
          if (_error != null) Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
        ]),
      ),
    ),
    actions: [
      TextButton(onPressed: _busy ? null : () => Navigator.of(context).pop(), child: const Text('Cancelar')),
      FilledButton(
        key: const Key('reporte-enviar'),
        onPressed: _busy ? null : _enviar, child: Text(_busy ? 'Enviando...' : 'Enviar reporte'),
      ),
    ],
  );
}
