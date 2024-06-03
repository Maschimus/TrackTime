import 'dart:async';
import 'package:flutter/material.dart';
import 'package:tracktime/controller/activity_controller.dart';

class CurrentActivity extends StatefulWidget {
  final String activityName;

  CurrentActivity({required this.activityName});

  @override
  State<CurrentActivity> createState() => _CurrentActivityPageState();
}

class _CurrentActivityPageState extends State<CurrentActivity> {
  final ActivityController _activityController = ActivityController();
  late Timer _timer;
  int _seconds = 0;
  final TextEditingController _textController = TextEditingController();
  late DateTime _startTime;
  String? _submittedComment;

  @override
  void initState() {
    super.initState();
    _startTime = DateTime.now();
    _startTimer();
  }

  @override
  void dispose() {
    _timer.cancel();
    _textController.dispose();
    super.dispose();
  }

  void _startTimer() {
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      setState(() {
        _seconds = DateTime.now().difference(_startTime).inSeconds;
      });
    });
  }

  String _formatDuration(int seconds) {
    final int hours = seconds ~/ 3600;
    final int minutes = (seconds % 3600) ~/ 60;
    final int secs = seconds % 60;
    return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  Future<void> _handleSubmit() async {
    final String comment = _textController.text;
    await _activityController.addComment(comment: comment);
    setState(() {
      _submittedComment = comment;
      _textController.clear();
    });
    print('Submitted comment: $comment');
  }

  @override
  Widget build(BuildContext context) {
    AppBar appBar = AppBar(
      leading: IconButton(
        icon: Icon(Icons.arrow_back, color: Colors.grey),
        onPressed: () => Navigator.of(context)
            .pushReplacementNamed('./activityselectionpage'),
      ),
      backgroundColor: Colors.white,
      title: const Text(
        "Time Tracking",
        style: TextStyle(color: Colors.grey),
      ),
      centerTitle: true,
      elevation: 0,
    );

    return Scaffold(
      appBar: appBar,
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                widget.activityName,
                style: const TextStyle(
                  fontSize: 24.0,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey,
                ),
              ),
              SizedBox(height: 20.0),
              Text(
                _formatDuration(_seconds),
                style: const TextStyle(
                  fontSize: 48.0,
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                ),
              ),
              if (_submittedComment != null) ...[
                SizedBox(height: 20.0),
                Text(
                  _submittedComment!,
                  style: TextStyle(
                    fontSize: 16.0,
                    color: Colors.grey,
                  ),
                ),
              ],
              SizedBox(height: 40.0),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40.0),
                child: TextField(
                  controller: _textController,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Enter text',
                  ),
                ),
              ),
              SizedBox(height: 20.0),
              ElevatedButton(
                onPressed: _handleSubmit,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding:
                      EdgeInsets.symmetric(horizontal: 32.0, vertical: 16.0),
                  textStyle: TextStyle(
                    fontSize: 20.0,
                    color: Colors.blue,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                child: Text(
                  'Submit',
                  style: TextStyle(color: Colors.grey[800]),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.of(context)
                        .pushReplacementNamed('./activityselectionpage');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    padding:
                        EdgeInsets.symmetric(horizontal: 32.0, vertical: 16.0),
                    textStyle: TextStyle(
                      fontSize: 20.0,
                      color: Colors.blue,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  child: Text(
                    'Activity List',
                    style: TextStyle(color: Colors.grey[800]),
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
