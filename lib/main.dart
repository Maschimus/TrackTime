import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tracktime/collections/activity.dart';
import 'package:tracktime/models/database/current_activity.dart';
import 'package:tracktime/models/database/isar.dart';
import 'routegenerator.dart';
import 'package:isar/isar.dart';
// Path
import 'package:path_provider/path_provider.dart';
// Get it locator
import 'package:get_it/get_it.dart';

// This is our global ServiceLocator
GetIt getIt = GetIt.instance;

Future main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final dir = await getApplicationSupportDirectory();
  final isar = await Isar.open([ActivitySchema], directory: dir.path);

  // Todo check comment above
  getIt.registerSingleton<IsarDataBase>(IsarDataBase());
  getIt.registerSingleton<CurrentActivityModel>(CurrentActivityModel());

  // Set isar
  getIt.get<IsarDataBase>().setIsar(isar);
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider<CurrentActivityModel>(
            create: (_) => getIt<CurrentActivityModel>()),
      ],
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/activityselectionpage',
      onGenerateRoute: RouteGenerator.generateRoute,
    );
  }
}
