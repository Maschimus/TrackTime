import 'package:isar/isar.dart';

class IsarDataBase {
  IsarDataBase();

  late Isar isar;

  void setIsar(Isar isarbase) {
    isar = isarbase;
    print("Set isar");
  }

  Isar get() {
    return isar;
  }
}
