$("span.glyphicon-chevron-up").on('click', (event) => {
	$(".rollbox-min").addClass("hidden");
	$(".rollbox").removeClass("hidden");
});

$("span.glyphicon-remove").on('click', (event) => {
	$(".rollbox").addClass("hidden");
	$(".rollbox-min").removeClass("hidden");
});

$("input.ipt-roll").keypress(function(e) {
	if (e.which == 13) {
		var diceCheck = /([1-9]\d*)?d([1-9]\d*)(\s?([+-])\s?(\d+))?/i;
		var result = $("input.ipt-roll").val().match(diceCheck);

		if ((result == null) && ($("input.ipt-roll").val() == "/help")) {
			/* Append Drop highest (`2d4dh1`) and lowest (`4d6dl1`) are supported.
Up and down arrow keys cycle input history.
Anything before a colon is treated as a label (`Fireball: 8d6`)
Use `/macro list` to list saved macros.
Use `/macro add myName 1d2+3` to add (or update) a macro. Macro names should not contain spaces or hashes.
Use `/macro remove myName` to remove a macro.
Use `#myName` to roll a macro.
Use `/clear` to clear the roller.*/
			$("div.out-roll").append("<p>Append Drop highest (<code>2d4dh1</code>) and lowest (<code>4d6dl1</code>) are supported.<br />Up and down arrow keys cycle input history.<br />Anything before a colon is treated as a label (<code>Fireball: 8d6</code>)<br />Use <code>/macro list</code> to list saved macros.<br />Use <code>macro add myName 1d2+3</code> to add (or update) a macro. Macro names should not contain spaces or hashes.<br />Use <code>/macro remove myName</code> to remove a macro.<br />Use <code>#myName</code> to roll a macro.<br />Use <code>/clear</code> to clear the roller.</p>");
		} else if ((result == null) && ($("input.ipt-roll").val() == "/clear")) {
			$("div.out-roll").text("");
		}

		$("input.ipt-roll").val("");
	}
});