$("body").append('<div class="rollbox-min"><span class="glyphicon glyphicon-chevron-up"></span></div><div class="rollbox hidden"><div class="head-roll"><span class="hdr-roll">Dice Roller</span><span class="delete-icon glyphicon glyphicon-remove"></span></div><div class="out-roll"></div><input class="ipt-roll" autocomplete="off" spellcheck="false" placeholder="3d6-1 or &quot;/help&quot;"></div>');

$("span.glyphicon-chevron-up").on('click', (event) => {
	$(".rollbox-min").addClass("hidden");
	$(".rollbox").removeClass("hidden");
});

$("span.glyphicon-remove").on('click', (event) => {
	$(".rollbox").addClass("hidden");
	$(".rollbox-min").removeClass("hidden");
});

function strip(str) {
    return str.replace(/^\s+|\s+$/g, '');
}

function parseCommand(cmd) {
	if (cmd == "/help") {
		$("div.out-roll").append("Drop highest (<code>2d4dh1</code>) and lowest (<code>4d6dl1</code>) are supported.<br />Up and down arrow keys cycle input history.<br />Anything before a colon is treated as a label (<code>Fireball: 8d6</code>)<br />Use <code>/macro list</code> to list saved macros.<br />Use <code>/macro add myName</code> to add (or update) a macro. Macro names should not contain spaces or hashes.<br />Use <code>/macro remove myName</code> to remove a macro.<br />Use <code>#myName</code> to roll a macro.<br />Use <code>/clear</code> to clear the roller.<br /><br />");
	} else if (cmd == "/clear") {
		$("div.out-roll").text("");
	} else if (cmd.startsWith("/macro")) {
		var args = cmd.split(" ");

		if (args[1] == "add") {
			var macro = "";

			for (var i = 3; i < args.length; i++) {
				macro += args[i];
				macro += " ";
			}

			macro = strip(macro);

			if (localStorage.getItem("macros") == null) {
				localStorage.setItem("macros", '{"macros":[{"' + args[2] + '": "' + macro + '"}]}');
			} else {
				var macros = JSON.parse(localStorage.getItem("macros"));

				for (var i = 0; i < macros.macros.length; i++) {
					if (Object.keys(macros.macros[i]).indexOf(args[2]) >= 0) {
						macros.macros[i][args[2]] = macro;
					}
				}

				localStorage.setItem("macros", JSON.stringify(macros));
			}

			$("div.out-roll").append("Successfully added " + args[2] + " macro.<br /><br />");
		} else if (args[1] == "remove") {
			if (localStorage.getItem("macros") == null) {
				$("div.out-roll").append("That macro does not exist.<br /><br />");
			} else {
				var macros = JSON.parse(localStorage.getItem("macros"));
				var i;

				for (i = 0; i < macros.macros.length; i++) {
					if (Object.keys(macros.macros[i]).indexOf(args[2]) >= 0) {
						break;
					}
				}

				delete macros.macros[i];
				localStorage.setItem("macros", JSON.stringify(macros));
				$("div.out-roll").append("Succesfully removed " + args[2] + " macro.<br /><br />");
			}
		} else if (args[1] == "list") {
			if (localStorage.getItem("macroList") == null) {
				$("div.out-roll").append("List of macros: <br /><br />");
			} else {
				var macros = JSON.parse(localStorage.getItem("macros"));

				$("div.out-roll").append("List of macros: ");

				for (var i = 0; i < macros.macros.length; i++) {
					$("div.out-roll").append(Object.keys(macros.macros[i])[0]);
				}

				$("div.out-roll").append("<br /><br />");
			}
		}
	}
}

function rollDie(dieType) {
	return Math.floor(Math.random() * (dieType - 1)) + 1;
}

function rollDice(dieAmount, dieType) {
	var data = {"sum": 0, "rolls": []}

	for (var i = 0; i < dieAmount; i++) {
		var roll = rollDie(dieType);
		data["sum"] += roll;
		data["rolls"].push(roll);
	}

	return data;
}

function processInput(input) {
	var diceCheck = /([1-9]\d*)?d([1-9]\d*)(\s?([+-])\s?(\d+))?/i;
	var result = input.match(diceCheck);
	var isCmd = input.startsWith("/");
	var isMacro = input.startsWith("#");

	if (isCmd) {
		parseCommand(input);
	} else if (isMacro) {
		parseMacro(input.replace("#", ""));
	} else if (!isCmd && !isMacro && result) {
		var rollData = rollDice(Number(result[1]), Number(result[2]));
		var critSuccess = false;
		var critFail = false;

		for (var i = 0; i < rollData.rolls.length; i++) {
			if (rollData.rolls[i] == Number(result[2])) {
				critSuccess = true;
			} else if (rollData.rolls[i] == 1) {
				critFail = true;
			}
		}

		if (result[3] == null) {
			if (critSuccess && !critFail) {
				$("div.out-roll").append('Result: <span class="roll-crit">' + String(rollData.sum) + '</span> (');
			} else if (critFail && !critSuccess) {
				$("div.out-roll").append('Result: <span class="roll-fail">' + String(rollData.sum) + '</span> (');
			} else if (critFail && critSuccess) {
				$("div.out-roll").append('Result: <span class="roll-mixed">' + String(rollData.sum) + '</span> (');
			} else {
				$("div.out-roll").append("Result: " + String(rollData.sum) + " (");
			}
		} else {
			if (critSuccess && !critFail) {
				$("div.out-roll").append('Result: <span class="roll-crit">' + String(rollData.sum + Number(result[3])) + '</span> (');
			} else if (critFail && !critSuccess) {
				$("div.out-roll").append('Result: <span class="roll-fail">' + String(rollData.sum + Number(result[3])) + '</span> (');
			} else if (critFail && critSuccess) {
				$("div.out-roll").append('Result: <span class="roll-mixed">' + String(rollData.sum + Number(result[3])) + '</span> (');
			} else {
				$("div.out-roll").append("Result: " + String(rollData.sum + Number(result[3])) + " (");
			}
		}

		if (rollData.rolls.length == 1) {
			if (result[3] == null) {
				if (rollData.rolls[0] == Number(result[2])) {
					$("div.out-roll").append('<span class="roll-crit">' + result[2] + '</span>)<br /><br />');
				} else if (rollData.rolls[0] == 1) {
					$("div.out-roll").append('<span class="roll-fail">1</span>)<br /><br />');
				} else {
					$("div.out-roll").append(String(rollData.rolls[0]) + ')<br /><br />');
				}
			} else {
				if (rollData.rolls[0] == Number(result[2])) {
					$("div.out-roll").append('<span class="roll-crit">' + result[2] + '</span> ' + result[4] + ' ' + result[5] + ')<br /><br />');
				} else if (rollData.rolls[0] == 1) {
					$("div.out-roll").append('<span class="roll-fail">1</span> ' + result[4] + ' ' + result[5] + ')<br /><br />');
				} else {
					$("div.out-roll").append(String(rollData.rolls[0]) + ' ' + result[4] + ' ' + result[5] + ')<br /><br />');
				}
			}
		} else {
			for (var i = 0; i < rollData.rolls.length - 1; i++) {
				if (rollData.rolls[i] == Number(result[2])) {
					$("div.out-roll").append('<span class="roll-crit">' + String(rollData.rolls[i]) + '</span> + ');
				} else if (rollData.rolls[i] == 1) {
					$("div.out-roll").append('<span class="roll-fail">1</span> + ');
				} else {
					$("div.out-roll").append(String(rollData.rolls[i]) + " + ");
				}
			}

			if (result[3] == null) {
				if (rollData.rolls[rollData.rolls.length - 1] == Number(result[2])) {
					$("div.out-roll").append('<span class="roll-crit">' + result[2] + '</span>)<br /><br />');
				} else if (rollData.rolls[rollData.rolls.length - 1] == 1) {
					$("div.out-roll").append('<span class="roll-fail">1</span>)<br /><br />');
				} else {
					$("div.out-roll").append(String(rollData.rolls[rollData.rolls.length - 1]) + ")<br /><br />");
				}
			} else {
				if (rollData.rolls[rollData.rolls.length - 1] == Number(result[2])) {
					$("div.out-roll").append('<span class="roll-crit">' + result[2] + '</span> ' + result[4] + ' ' + result[5] + ')<br /><br />');
				} else if (rollData.rolls[rollData.rolls.length - 1] == 1) {
					$("div.out-roll").append('<span class="roll-fail">1</span> ' + result[4] + ' ' + result[5] + ')<br /><br />');
				} else {
					$("div.out-roll").append(String(rollData.rolls[rollData.rolls.length - 1]) + " " + result[4] + " " + result[5] + ")<br /><br />");
				}
			}
		}
	}
	
	$("div.out-roll").scrollTop($("div.out-roll")[0].scrollHeight);
}

function parseMacro(macro) {
	if (localStorage.getItem("macros") == null) {
		$("div.out-roll").append("That macro does not exist.<br /><br />");
	} else {
		var macros = JSON.parse(localStorage.getItem("macros"));

		for (var i = 0; i < macros.macros.length; i++) {
			if (Object.keys(macros.macros[i]).indexOf(macro) >= 0) {
				processInput(macros.macros[i][macro]);
			}
		}
	}
}

$("input.ipt-roll").keydown(function(e) {
	if (e.which == 13) {
		// Enter key
		processInput($("input.ipt-roll").val());

		if (sessionStorage.getItem("diceHistory") == null) {
			sessionStorage.setItem("diceHistory", '{"history": [' + $("input.ipt-roll").val() + ']}')
		} else {
			var diceHistory = JSON.parse(sessionStorage.getItem("diceHistory"));
			diceHistory.history.push($("input.ipt-roll").val());
			sessionStorage.setItem("diceHistory", JSON.stringify(diceHistory));
		}

		$("input.ipt-roll").val("");
	} else if (e.which == 38) {
		// Up arrow key

		if (sessionStorage.getItem("diceHistory") != null) {
			var diceHistory = JSON.parse(sessionStorage.getItem("diceHistory"));

			if (Object.keys(diceHistory).indexOf("historyID") < 0) {
				diceHistory.historyID = diceHistory.history.length - 1;
			} else {
				if (diceHistory.historyID > 0) {
					diceHistory.historyID -= 1;
				}
			}

			$("input.ipt-roll").val(diceHistory.history[diceHistory.historyID]);
			sessionStorage.setItem("diceHistory", JSON.stringify(diceHistory));
		}
	} else if (e.which == 40) {
		// Down arrow key

		if (sessionStorage.getItem("diceHistory") != null) {
			var diceHistory = JSON.parse(sessionStorage.getItem("diceHistory"));
			var clear = false;

			if ((Object.keys(diceHistory).indexOf("historyID") >= 0) && (diceHistory.historyID < (diceHistory.history.length - 1))) {
				diceHistory.historyID += 1;
			} else if ((Object.keys(diceHistory).indexOf("historyID") >= 0) && (diceHistory.historyID == (diceHistory.history.length - 1))) {
				clear = true;
			}

			if (clear) {
				$("input.ipt-roll").val("");
			} else {
				$("input.ipt-roll").val(diceHistory.history[diceHistory.historyID]);
			}
			
			sessionStorage.setItem("diceHistory", JSON.stringify(diceHistory));
		}
	}
});