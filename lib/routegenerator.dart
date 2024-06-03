import 'package:flutter/material.dart';
import 'package:tracktime/pages/current_activity_page.dart';
import 'package:tracktime/pages/activitySelectionPage.dart';

class RouteGenerator {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    // Getting arguments passed in while calling Navigator.pushNamed
    final args = settings.arguments;

    switch (settings.name) {
      // menus
      case '/':
        return MaterialPageRoute(builder: (_) => ActivitySelectionPage());

      case '/currentactivitypage':
        return MaterialPageRoute(
            builder: (_) => CurrentActivity(activityName: args as String));
      case '/activityselectionpage':
        return MaterialPageRoute(builder: (_) => ActivitySelectionPage());

      default:
        return MaterialPageRoute(builder: (_) => ActivitySelectionPage());
    }
  }
}
