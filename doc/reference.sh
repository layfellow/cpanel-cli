#!/usr/bin/env bash

cat << EOS
=================
Command Reference
=================

\`Leer en español </es/latest/reference.html>\`_

EOS

while read line; do
	line="${line//‘\\n’/\`\`\\n\`\`}"
	line="${line//‘\\t’/\`\`\\t\`\`}"

	if [[ $line =~ ^Usage:\ cpanel\ ([a-z]+)\ ([a-z]+) ]]; then
		echo "Module: \`\`${BASH_REMATCH[2]}\`\`"
		echo -e "==================================================\n"
		[[ $line =~ ^Usage:\ cpanel\ (.+) ]]
		echo -e "- **${BASH_REMATCH[1]}**\n"

	elif [[ $line =~ ^\ *cpanel\ (.+) ]]; then
		echo -e "- **${BASH_REMATCH[1]}**\n"

	elif [[ $line =~ ^\ *EXAMPLES ]]; then
		echo -e "*Examples*\n\n.. code:: sh\n"

	elif [[ $line =~ ^\ *EXAMPLE ]]; then
		echo -e "*Example*\n\n.. code:: sh\n"

	elif [[ $line =~ ^\ *033\[1m(.+)033\[0m ]]; then
		echo -e "**${BASH_REMATCH[1]}**\n"

	elif [[ $line =~ ^\ *033\[1\;34m(.+)033\[00m ]]; then
		echo "    \$ ${BASH_REMATCH[1]}"

	elif [[ $line =~ ^\ *033\[1\;34m(.+)032\[00m ]]; then
		echo "    \$ ${BASH_REMATCH[1]}"

	elif [[ $line =~ ^--- ]]; then
		echo -n ""

	else
		echo "$line"
	fi
done < $1
