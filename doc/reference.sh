#!/usr/bin/env bash

# Generate doc/reference.rst and doc/reference/*.rst from cpanel/USAGE

cat << EOS > "${2}".rst
..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

=================
Command Reference
=================

\`Leer en español </es/latest/reference.html>\`_

.. toctree::
   :maxdepth: 3

EOS

while read -r line; do
	if [[ $line =~ ^Usage:\ cpanel\ ([a-z]+)\ ([a-z]+) ]]; then
		if [ "${BASH_REMATCH[2]}" != "$module" ]; then
			module="${BASH_REMATCH[2]}"
			echo "   reference/${BASH_REMATCH[2]}" >> "${2}.rst"
		fi
	fi
done < "$1"

mkdir -p "./${2}"
module=""

while read -r line; do
	line="${line//\\\\n/\\n}"
	line="${line//\\\\t/\\t}"
	line="${line//\\\'/\'}"
	line="${line//USER@DOMAIN/USER\\@DOMAIN}"

	if [[ $line =~ ^Usage:\ cpanel\ ([a-z]+)\ ([a-z]+) ]]; then
		if [ "${BASH_REMATCH[2]}" != "$module" ]; then
			module="${BASH_REMATCH[2]}"
			cat <<- EOS > "${2}/${module}.rst"
			..
			   Do not edit this .rst file directly — it’s generated programmatically.
			   See doc/reference.sh.

			==================================================
			Module: \`\`${module}\`\`
			==================================================

			\`Leer en español </es/latest/reference/${module}.html>\`_

			EOS
		fi
		# HACK  Print subtitles for mail and dir modules only
		[[ $line =~ ^Usage:\ cpanel\ ([a-z]+)\ ([a-z]+)\ ([a-z]+) ]]
		if [ -n "${BASH_REMATCH[3]}" ] &&

			[[ "$module" == "dir" || "$module" == "mail" ]]
		then
			cat <<- EOS >> "${2}/${module}.rst"

			\`\`${BASH_REMATCH[3]}\`\`
			==================================================

			EOS
		fi

		[[ $line =~ ^Usage:\ cpanel\ (.+) ]]
		echo "- **${BASH_REMATCH[1]}**" >> "${2}/${module}".rst

	elif [[ $line =~ ^\ *cpanel\ (.+) ]]; then
		echo "- **${BASH_REMATCH[1]}**" >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *EXAMPLES ]]; then
		echo -e "*Examples*\n\n.. code:: sh\n" >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *EXAMPLE ]]; then
		echo -e "*Example*\n\n.. code:: sh\n" >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *\\033\[1\;34mcpanel\ (.+)\ \\\\\ \\033\[00m ]]; then
		echo "    \$ cpanel ${BASH_REMATCH[1]} \\ " >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *\\033\[1\;34mcpanel\ (.+)\\033\[00m ]]; then
		echo "    \$ cpanel ${BASH_REMATCH[1]}" >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *\\033\[1\;34m\ +(.+)\ \\\\\ \\033\[00m ]]; then
		echo "          ${BASH_REMATCH[1]} \\ " >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *\\033\[1\;34m\ +(.+)\\033\[00m ]]; then
		echo "          ${BASH_REMATCH[1]}" >> "${2}/${module}.rst"

	elif [[ $line =~ ^\ *\\033\[1m(.+)\\033\[0m ]]; then
		echo -e "**${BASH_REMATCH[1]}**\n" >> "${2}/${module}.rst"

	elif [[ $line =~ ^--- ]]; then
		echo -n "" >> "${2}/${module}.rst"

	else
		echo "$line" >> "${2}/${module}.rst"
	fi
done < "$1"
