String formatoPrecio(double value) {
  final parts = value.toStringAsFixed(2).split('.');
  final digits = parts.first;
  final buffer = StringBuffer();
  for (var i = 0; i < digits.length; i++) {
    if (i > 0 && (digits.length - i) % 3 == 0) buffer.write('.');
    buffer.write(digits[i]);
  }
  final whole = buffer.toString();
  final decimals = parts.last == '00' ? '' : ',${parts.last}';
  return 'COP \$$whole$decimals';
}
