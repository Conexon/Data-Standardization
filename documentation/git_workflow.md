# Git Workflow and Commands

### Generate a SSH key and add it to GitHub 
(should only need to do this once)

  * Generate a SSH key - https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
  
  * Add SSH key to GitHub - https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
  
  * Adding a passphrase is suggested (write it down somewhere)
  
### Clone a repository 
(only need to do this once for every new repo you want to clone to your local machine)

  * In terminal, navigate (cd) to a folder that will store your Git code (I keep mine in a folder called “githome”)

  * Go to a GitHub repo and find the green box that says “code” and copy the URL under SSH

(image)

  * In terminal, issue the command `git clone` and paste the URL from GitHub
  
### Create a new branch
  
  * cd to a local repo
  
  * Make sure you are on the default branch (depends on the repo, most are `master` some are `develop` - the git web site will tell you what the default branch is on the `code` page with the drop down for branch. the one with the check box is the default branch (again, usually master). You can check to make sure you are on the default branch by issuing the command `git branch`

  * From the default branch, issue the command `git pull` to grab any recent changes that your teammates have made to the repo.
  
  *	From the default branch, issue the command `git checkout -b <new_branch_name>`
  
    *	this gives you a new branch where you want to make edits.
    
  *	Open Sublime (or another text editor) and edit your code, saving frequently.

    *	Link to download Sublime Text: https://www.sublimetext.com/ 
    
  *	If you don't like the edits you can; you can delete them, w/o making any change to the default code
  
    *	`git stash`
    
    *	`git checkout master`
    
    *	`git branch -d <new_branch_name>`
    
  *	If you want to save your edits and make them as a suggestion to the repo everyone uses

    *	`git status` - this will show you the files that you have changed
    *	`git add *`
    *	`git commit -m ‘some comment'`
    *	`git push` - this will push it to the git web site - you will actually have to use this upstream switch that git tells you specifically what to do
    *	Then go to the git page for that repo, and open a pull request for the changes you want to make
      *	Make sure there is a conversation amongst your teammates about these changes. **Your changes affect all people on the team.**
