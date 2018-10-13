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
		<th>Creates the genetic algorithm based on desired pool size (cars) and passes in Neural Network (individual for each car).</th>
	</tr>
	<tr>
		<th>3.</th>
		<th>Call genetic algorithm creation function.<th/>
		<th>Calls construct within genetic algorithm that either creates/mutates/crossover best car candidate. Creation is top priority if cars have no set genes.</th>
	</tr>
	<tr>
		<th>4.</th>
		<th>Retrieve cars generated.</th>
		<th>Cars generated from previous creation are gathered and spawned into the level.</th>
	</tr>
</table>


