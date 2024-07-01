import liveplugin.show
import java.io.File

show("Hello")

// Define the virtual environment's Python interpreter
val venvPython = "H:/Documents/Apply/Applications/TU Delft/Assessment/test-assignment/venv/Scripts/python.exe"

// Define the Python script file
val pythonScript = "H:/Documents/Apply/Applications/TU Delft/Assessment/test-assignment/detection/trace_classifier/long_traces.py"
// Build the command to run the Python script using the virtual environment's Python interpreter
val command = listOf(venvPython, pythonScript)

val customCodePath = "H:/Documents/Apply/Applications/TU Delft/Assessment/test-assignment/"  // Replace with your custom directory

// Set the environment variable for PYTHONPATH to include the virtual environment's site-packages
val env = mutableMapOf<String, String>()
env.putAll(System.getenv()) // Copy current environment variables
env["PYTHONPATH"] = customCodePath
show(env["PYTHONPATH"])

// Execute the command
val processBuilder = ProcessBuilder(command)
processBuilder.environment().putAll(env) // Add the PYTHONPATH to the environment
processBuilder.redirectErrorStream(true)
val process = processBuilder.start()

// Capture the output of the script
val output = process.inputStream.bufferedReader().use { it.readText() }

// Wait for the process to finish
val exitCode = process.waitFor()

// Print the output and exit code
show("Output:\n$output")
show("Exit code: $exitCode")