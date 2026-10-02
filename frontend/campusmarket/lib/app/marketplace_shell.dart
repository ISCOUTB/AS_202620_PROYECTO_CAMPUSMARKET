import 'package:flutter/material.dart';

import '../catalogo/catalogo_page.dart';
import '../publicaciones/publicacion_form_page.dart';
import 'inicio_page.dart';

class MarketplaceShell extends StatefulWidget {
  const MarketplaceShell({super.key});

  @override
  State<MarketplaceShell> createState() => _MarketplaceShellState();
}

class _MarketplaceShellState extends State<MarketplaceShell> {
  int _indice = 0;

  void _irInicio() => setState(() => _indice = 0);
  void _irCatalogo() => setState(() => _indice = 1);
  void _irPublicar() => setState(() => _indice = 2);

  void _seleccionar(int indice) {
    if (indice == _indice) return;
    setState(() => _indice = indice);
  }

  @override
  Widget build(BuildContext context) {
    final paginas = [
      InicioPage(onIrCatalogo: _irCatalogo, onIrPublicar: _irPublicar),
      const CatalogoPage(),
      const PublicacionFormPage(),
    ];

    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth;
        final desktop = width >= 1100;
        final tablet = width >= 700 && width < 1100;

        if (desktop) {
          return Scaffold(
            appBar: AppBar(
              toolbarHeight: 76,
              titleSpacing: 32,
              title: InkWell(
                borderRadius: BorderRadius.circular(14),
                onTap: _irInicio,
                child: const Padding(
                  padding: EdgeInsets.symmetric(vertical: 6),
                  child: _CampusMarketBrand(),
                ),
              ),
              actions: [
                _DesktopNavButton(
                  icon: Icons.home_outlined,
                  label: 'Inicio',
                  selected: _indice == 0,
                  onPressed: _irInicio,
                ),
                const SizedBox(width: 6),
                _DesktopNavButton(
                  icon: Icons.storefront_outlined,
                  label: 'Catálogo',
                  selected: _indice == 1,
                  onPressed: _irCatalogo,
                ),
                const SizedBox(width: 6),
                _DesktopNavButton(
                  icon: Icons.add_circle_outline,
                  label: 'Publicar',
                  selected: _indice == 2,
                  onPressed: _irPublicar,
                ),
                const SizedBox(width: 24),
              ],
            ),
            body: IndexedStack(index: _indice, children: paginas),
          );
        }

        if (tablet) {
          return Scaffold(
            appBar: AppBar(
              titleSpacing: 20,
              title: InkWell(
                borderRadius: BorderRadius.circular(14),
                onTap: _irInicio,
                child: const _CampusMarketBrand(compact: true),
              ),
            ),
            body: Row(
              children: [
                NavigationRail(
                  selectedIndex: _indice,
                  onDestinationSelected: _seleccionar,
                  labelType: NavigationRailLabelType.all,
                  groupAlignment: -0.75,
                  leading: Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: IconButton.filledTonal(
                      tooltip: 'Publicar producto',
                      onPressed: _irPublicar,
                      icon: const Icon(Icons.add),
                    ),
                  ),
                  destinations: const [
                    NavigationRailDestination(
                      icon: Icon(Icons.home_outlined),
                      selectedIcon: Icon(Icons.home),
                      label: Text('Inicio'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.storefront_outlined),
                      selectedIcon: Icon(Icons.storefront),
                      label: Text('Catálogo'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.add_circle_outline),
                      selectedIcon: Icon(Icons.add_circle),
                      label: Text('Publicar'),
                    ),
                  ],
                ),
                const VerticalDivider(width: 1),
                Expanded(
                  child: IndexedStack(index: _indice, children: paginas),
                ),
              ],
            ),
          );
        }

        return Scaffold(
          appBar: AppBar(
            titleSpacing: 16,
            title: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: _irInicio,
              child: const _CampusMarketBrand(compact: true),
            ),
            actions: [
              IconButton(
                tooltip: 'Publicar producto',
                onPressed: _irPublicar,
                icon: const Icon(Icons.add_circle_outline),
              ),
              const SizedBox(width: 8),
            ],
          ),
          body: IndexedStack(index: _indice, children: paginas),
          bottomNavigationBar: NavigationBar(
            selectedIndex: _indice,
            onDestinationSelected: _seleccionar,
            destinations: const [
              NavigationDestination(
                icon: Icon(Icons.home_outlined),
                selectedIcon: Icon(Icons.home),
                label: 'Inicio',
              ),
              NavigationDestination(
                icon: Icon(Icons.storefront_outlined),
                selectedIcon: Icon(Icons.storefront),
                label: 'Catálogo',
              ),
              NavigationDestination(
                icon: Icon(Icons.add_circle_outline),
                selectedIcon: Icon(Icons.add_circle),
                label: 'Publicar',
              ),
            ],
          ),
        );
      },
    );
  }
}

class _CampusMarketBrand extends StatelessWidget {
  const _CampusMarketBrand({this.compact = false});

  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Semantics(
      button: true,
      label: 'CampusMarket, ir al inicio',
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: compact ? 38 : 42,
            height: compact ? 38 : 42,
            decoration: BoxDecoration(
              color: colors.primaryContainer,
              borderRadius: BorderRadius.circular(13),
            ),
            child: Icon(Icons.school_outlined, color: colors.primary),
          ),
          const SizedBox(width: 11),
          RichText(
            text: TextSpan(
              style:
                  (compact
                          ? theme.textTheme.titleMedium
                          : theme.textTheme.titleLarge)
                      ?.copyWith(fontWeight: FontWeight.w900),
              children: [
                TextSpan(
                  text: 'Campus',
                  style: TextStyle(color: colors.onSurface),
                ),
                TextSpan(
                  text: 'Market',
                  style: TextStyle(color: colors.primary),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _DesktopNavButton extends StatelessWidget {
  const _DesktopNavButton({
    required this.icon,
    required this.label,
    required this.selected,
    required this.onPressed,
  });

  final IconData icon;
  final String label;
  final bool selected;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;

    return TextButton.icon(
      onPressed: onPressed,
      icon: Icon(icon),
      label: Text(label),
      style: TextButton.styleFrom(
        foregroundColor: selected ? colors.primary : colors.onSurfaceVariant,
        backgroundColor: selected
            ? colors.primaryContainer.withValues(alpha: 0.55)
            : Colors.transparent,
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 15),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
    );
  }
}
