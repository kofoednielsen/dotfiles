# This script is used to set PS1 in an interactive zsh terminal.
#
# You probably want to fork/modify based on your preferences.
#
# MIT licensed.


# Zsh references:
# https://zsh.sourceforge.io/Doc/Release/Functions.html#Hook-Functions
# https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html#Prompt-Expansion
# https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Character-Highlighting


ps1_precmd() {
    # A red exit code, if last command failed.
    if [ "$?" = "0" ]; then
        status_msg=""
    else
        status_msg="$? "
    fi

    # Are we in a git repo?
    if git rev-parse 2>/dev/null; then
        if [ -z "$(git status --porcelain)" ]; then
          git_clean_indicator=""  # Working directory clean
        else
          git_clean_indicator=" ✘"  # Uncommitted changes
        fi
        ref_name=$(git name-rev --name-only --always HEAD)
        git_prompt=" ${ref_name}${git_clean_indicator}"
    else
        git_prompt=""
    fi

    cwd_prompt='\w'
    if [ "$(id -u)" = "0" ]; then
        # If UID is 0, print "root" in red.
        cwd_prompt="root ${cwd_prompt}"
    fi

    PS1="${status_msg}$(hostname)@ ${cwd_prompt}${git_prompt} ❯ "
}

PROMPT_COMMAND="ps1_precmd"
