# CSC434AIFinalProject
The capstone project using Artificially Intelligent systems.

<h2>The Project</h2>

<p>Using a Genetic Algorithm and a Neural Network, create a system that can maneuver a track.
</p>

<h3>Dependencies</h3>
<i>requirements.txt also takes care of all required pip dependencies</i>
<table>
	<tr>
		<th>Application/Module</td>
		<th>Command</th>
	</tr>
	<tr>
		<td>Python 3</td><td>sudo apt install python3</td>
	</tr>
	<tr>
		<td>Pip (Module installations)</td><td>sudo apt install python3-pip</td>
	</tr>
	<tr>
		<td>Numpy</td><td>pip install numpy</td>
	</tr>
	<tr>
		<td>Pygame</td><td>pip install pygame</td>
	</tr>
</table>

<h3>main.py</h3>
<table>
	<tr>
		<th>Order #</th>
		<th>Instruction</th>
		<th>Description</th>
	</tr>
	<tr>
		<th>0.</th>
		<th>Initialize main.py.</th>
		<th>Create the main container, houses algorithmic structure.</th>
	</tr>
	<tr>
		<th>1.</th>
		<th>Load level.</th>
		<th>Level chosen is based on level order selected, randomized each time main.py is initialized.<th>
	</tr>
	<tr>
		<th>2.</th>
		<th>Initialize Genetic Algorithm approach.</th>
		<th>Creates the genetic algorithm based on desired pool size (cars) and passes in Neural Network (individual for each car along with neuron sizing).</th>
	</tr>
	<tr>
		<th>3.</th>
		<th>Call genetic algorithm creation function.</th>
		<th>Calls construct within genetic algorithm that either creates/mutates/crossover best car candidate. Creation is top priority if cars have no set genes.</th>
	</tr>
	<tr>
		<th>4.</th>
		<th>Retrieve cars generated.</th>
		<th>Cars generated from previous creation are gathered and spawned into the level.</th>
	</tr>
	<tr>
		<th>5.</th>
		<th><b>Loop.</b></th>
		<th>Begin looping of algorithm by first iterating through each car in order for a decision to be made.</th>
	</tr>
	<tr>
		<th>6.</th>
		<th>Retrieve data for each car.</th>
		<th>Obtain the data from the get_car_data function. Returns tuple ((x,y), speed, direction, distance). Distance is merely a possible evaluation but rather used to grade fitness.</th>
	</tr>
	<tr>
		<th>6.</th>
		<th>Decide best move.</th>
		<th>Apply data gathered into prediction model for network by calling car decision(data).</th>
	</tr>
	<tr>
		<th>7.</th>
		<th>Apply move.</th>
		<th>Applies move by gathering outputs from decision function.</th>
	</tr>
	<tr>
		<th>8.</th>
		<th>Check/Update car.</th>
		<th>Check if the car needs to be removed and remove from the game, call genetic.py fitness to evaluate car's performance.</th>
	</tr>
	<tr>
		<th>9.</th>
		<th><b>Repeat.</b></th>
		<th>Repeat loop.</th>
		<th></th>
	</tr>
</table>



