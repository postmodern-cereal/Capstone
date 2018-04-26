from World_2 import World_2
world = World_2(19, 27)
print("Agent location:", world.agentx, ", ", world.agenty)
print("Actual world:")
world.display_world()
world.set_agentdir("d")
world.agent.add_data(world.sense_init())
world.agent.display_memory()
#world.simulate(1)
