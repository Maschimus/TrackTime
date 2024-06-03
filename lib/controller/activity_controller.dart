import 'dart:io';
import 'package:flutter/material.dart';
import 'package:isar/isar.dart';
import 'package:tracktime/collections/activity.dart';
import 'package:tracktime/main.dart';
import 'package:tracktime/models/database/current_activity.dart';
import 'package:tracktime/models/database/isar.dart';
import 'package:csv/csv.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share/share.dart';
import 'package:intl/intl.dart'; // Add this import for date formatting

class ActivityController with ChangeNotifier {
  ActivityController();

  final Isar isar = getIt.get<IsarDataBase>().get();

  // Log an activity (Create)
  Future<void> logActivity({required String activity}) async {
    final DateTime now = DateTime.now();
    final activityLog = Activity(
      name: activity,
      timeStamp: now,
      description: '',
    );

    await isar.writeTxn(() async {
      await isar.activitys.put(activityLog);
    });

    getIt<CurrentActivityModel>().currentActivity = activity;
    notifyListeners();
  }

  // Add a comment to the last activity
  Future<void> addComment({required String comment}) async {
    // Fetch the last activity entry from the database
    final lastActivity =
        await isar.activitys.where().sortByTimeStampDesc().findFirst();

    if (lastActivity != null) {
      // Update the entry with the new comment
      lastActivity.description = comment;

      // Save the updated entry back to the database
      await isar.writeTxn(() async {
        await isar.activitys.put(lastActivity);
      });
    }
  }

  // Export activities to CSV
  Future<void> exportToCSV() async {
    // Retrieve all activities from the database
    final activities = await isar.activitys.where().findAll();

    // Convert activities to a list of lists for CSV
    List<List<dynamic>> rows = [
      ["ID", "Name", "TimeStamp", "Description"]
    ];

    for (var activity in activities) {
      rows.add([
        activity.measurementId, // Assuming id is the primary key field name
        activity.name,
        activity.timeStamp.toIso8601String(),
        activity.description
      ]);
    }

    // Convert the list of lists to CSV
    String csvData = const ListToCsvConverter().convert(rows);

    // Get the application documents directory
    final directory = await getApplicationDocumentsDirectory();

    // Add a timestamp to the file name
    String timestamp = DateFormat('yyyyMMdd_HHmmss').format(DateTime.now());
    final path = '${directory.path}/activities_$timestamp.csv';

    // Write the CSV data to a file
    final file = File(path);
    await file.writeAsString(csvData);

    // Share the CSV file
    Share.shareFiles([path], text: 'Here is my activity log CSV file.');
  }

  // Delete the database
  Future<void> deleteDatabase() async {
    await isar.writeTxn(() async {
      await isar.activitys.clear();
    });
    notifyListeners();
  }
}
