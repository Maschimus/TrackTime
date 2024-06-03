import 'package:flutter/material.dart';

class CurrentActivityModel with ChangeNotifier {
  String _currentActivity = '';

  String get currentActivity => _currentActivity;

  set currentActivity(String activity) {
    _currentActivity = activity;
    notifyListeners();
  }

  // Singleton implementation
  static final CurrentActivityModel _instance =
      CurrentActivityModel._internal();

  factory CurrentActivityModel() {
    return _instance;
  }

  CurrentActivityModel._internal();
}
