import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tracktime/controller/activity_controller.dart';
import 'package:tracktime/models/database/current_activity.dart';

class ActivitySelectionPage extends StatefulWidget {
  @override
  State<ActivitySelectionPage> createState() => _ActivitySelectionPageState();
}

class _ActivitySelectionPageState extends State<ActivitySelectionPage> {
  final ActivityController _activityController = ActivityController();

  @override
  void initState() {
    super.initState();
  }

  // Method to create a button with a given label and color
  Widget _buildActivityButton(String label, Color color) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
          vertical: 5.0), // Adjust vertical padding as needed
      child: ElevatedButton(
        onPressed: () async {
          _activityController.logActivity(activity: label);
          if (label != "Feierabend") {
            Navigator.of(context)
                .pushNamed('/currentactivitypage', arguments: label);
          }
        },
        style: ElevatedButton.styleFrom(backgroundColor: color),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 16,
            color: Colors.grey[800],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final currentActivityModel = Provider.of<CurrentActivityModel>(context);
    final currentActivity = currentActivityModel.currentActivity;

    AppBar appBar = AppBar(
      // Add a leading icon here,
      backgroundColor: Colors.white,
      title: const Text(
        "Time Tracking",
        style: TextStyle(color: Colors.grey),
      ),
      centerTitle: true,
      elevation: 0,
      actions: [
        IconButton(
          icon: Icon(Icons.arrow_forward, color: Colors.grey),
          onPressed: () {
            Navigator.pushReplacementNamed(
              context,
              '/currentactivitypage',
              arguments: currentActivity,
            );
          },
        ),
      ],
    );
    return Scaffold(
      appBar: appBar,
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(10.0),
          child: Column(
            children: [
              _buildActivityButton("Meeting",
                  currentActivity == "Meeting" ? Colors.blue : Colors.grey),
              _buildActivityButton("Mails",
                  currentActivity == "Mails" ? Colors.blue : Colors.grey),
              _buildActivityButton("Patents",
                  currentActivity == "Patents" ? Colors.blue : Colors.grey),
              _buildActivityButton(
                  "Organisation",
                  currentActivity == "Organisation"
                      ? Colors.blue
                      : Colors.grey),
              _buildActivityButton("Planning",
                  currentActivity == "Planning" ? Colors.blue : Colors.grey),
              _buildActivityButton("Software",
                  currentActivity == "Software" ? Colors.blue : Colors.grey),
              _buildActivityButton("Hardware",
                  currentActivity == "Hardware" ? Colors.blue : Colors.grey),
              _buildActivityButton("Personal",
                  currentActivity == "Personal" ? Colors.blue : Colors.grey),
              _buildActivityButton("Other",
                  currentActivity == "Other" ? Colors.blue : Colors.grey),
              _buildActivityButton(
                  "HR", currentActivity == "HR" ? Colors.blue : Colors.grey),
              _buildActivityButton("Break",
                  currentActivity == "Break" ? Colors.blue : Colors.grey),
              _buildActivityButton("Feierabend",
                  currentActivity == "Feierabend" ? Colors.blue : Colors.grey),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(
                    vertical: 40.0), // Adjust vertical padding as needed
                child: ElevatedButton(
                  onPressed: () async {
                    _activityController.exportToCSV();
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                  child: Text(
                    "Export to CSV",
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.grey[900],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
