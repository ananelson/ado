from ado.portfolio import Portfolio
from ado.recipe import Recipe
from ado.step import Step
from ado.step import DoingRecipe
from ado.step import DoingStep
from datetime import datetime
import ado.commands
import sys

def do_command(r=False):
    """
    Do a recipe.
    """
    c = ado.commands.conn()
    if not r:
        Recipe.printall(c)
        raw_r = ado.commands.clean_input("Choose a recipe number: ")
        if raw_r:
            r = int(raw_r)
        else:
            sys.stderr.write("No recipe chosen.\n")
            sys.exit(1)

    print "You chose recipe '%s'" % r
    recipe = Recipe.get(c, r)
    print recipe.description

    doing = DoingRecipe.create(
            c,
            started_at = datetime.now(),
            recipe_id=recipe.id)

    for i, step in enumerate(recipe.steps()):
        started_at = datetime.now()
        print "Step %s) %s" % (i+1, step.description)
        description = ado.commands.clean_input("notes> ")
        completed_at = datetime.now()
        elapsed = completed_at - started_at
        print "Completed Step %s in %s" % (i+1, elapsed)
        DoingStep.create(c,
                started_at = started_at,
                completed_at = completed_at,
                step_description = step.description,
                description = description,
                step_id = step.id,
                doing_recipe_id = doing.id)

def recipe_command():
    """
    Create a new recipe with steps.
    """
    c = ado.commands.conn()
    created_at = datetime.now()

    print "Creating a new recipe."

    Portfolio.printall(c)
    portfolio_id = int(ado.commands.clean_input("Enter portfolio id: "))

    # Verify portfolio choice.
    portfolio = Portfolio.get(c, portfolio_id)
    print "You chose portfolio %s - %s" % (portfolio.id, portfolio.name)

    name = ado.commands.clean_input("Enter short name for recipe: ")
    print "Name set to '%s'" % name
    description = ado.commands.clean_input("Description of recipe: ")
    print "Description set to '%s'" % description
    print "Describe each step in the recipe you wish to define."
    step = 0
    steps = []
    while True:
        step += 1
        step_text = ado.commands.clean_input("Step %s: " % step)
        if step_text:
            steps.append(step_text)
            print "Processing step text '%s'" % step_text
        else:
            print "done! %s steps recorded." % len(steps)
            break

    print "How often should you do this recipe (e.g. 1w (1 week), 1d (1 day), 12h (12 hours), 30m (30 minutes)"
    raw_frequency = ado.commands.clean_input("> ")
    if raw_frequency:
        frequency = raw_frequency
        print "This recipe should be done every %s days" % frequency
    else:
        frequency = "None"
        print "No specified frequency."

    context = ado.commands.clean_input("Context (where you can do this): ")
    recipe = Recipe.create(
            c,
            context=context,
            created_at=created_at,
            description=description,
            frequency=frequency,
            name=name,
            portfolio_id=portfolio_id
            )

    print "Created recipe", recipe.id
    for step_text in steps:
        step = Step.create(
                c,
                created_at=created_at,
                recipe_id = recipe.id,
                description = step_text
                )
        print "Created step id %s" % step.id
