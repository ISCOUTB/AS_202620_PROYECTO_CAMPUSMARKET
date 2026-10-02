class PublicacionCatalogo {
  const PublicacionCatalogo({
    required this.id,
    required this.titulo,
    required this.descripcion,
    required this.precio,
    required this.modalidad,
    required this.estado,
  });

  final int id;
  final String titulo;
  final String descripcion;
  final double precio;
  final String modalidad;
  final String estado;

  factory PublicacionCatalogo.fromJson(Map<String, dynamic> json) {
    return PublicacionCatalogo(
      id: json['id'] as int,
      titulo: json['titulo'] as String,
      descripcion: json['descripcion'] as String,
      precio: (json['precio'] as num).toDouble(),
      modalidad: json['modalidad'] as String,
      estado: json['estado'] as String,
    );
  }
}
