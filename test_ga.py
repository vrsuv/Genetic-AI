import unittest
import population
import simulation 
import genome 
import creature 
import numpy as np
 
class TestGA(unittest.TestCase):
    def testBasicGA(self):
        pop = population.Population(pop_size=50, 
                                    gene_count=3)
        sim = simulation.ThreadedSim(pool_size=1)
        sim = simulation.Simulation()

        for iteration in range(10):
            sim.eval_population(pop, 2400)
            fits = [cr.get_distance_travelled() 
                    for cr in pop.creatures]
            links = [len(cr.get_expanded_links()) 
                    for cr in pop.creatures]
            print(
                iteration,
                "fittest:", np.round(np.max(fits), 3), 
                "mean_ftn:", 
                np.round(np.mean(fits), 3), 
                "mean_links:", np.round(np.mean(links)), 
                "max_links:", np.round(np.max(links))
                  )
            # print(np.round(np.mean(fits), 3))
            fit_map = population.Population.get_fitness_map(fits)
            new_creatures = [] # new generation
            for i in range(len(pop.creatures)):
                # get parents from roulette wheel selection
                p1_ind = population.Population.select_parent(fit_map)
                p2_ind = population.Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
                dna = genome.Genome.crossover(p1.dna, p2.dna)
                # mutate the DNA (gene) now
                dna = genome.Genome.point_mutate(dna, rate=0.1, amount=0.25)
                dna = genome.Genome.shrink_mutate(dna, rate=0.25)
                dna = genome.Genome.grow_mutate(dna, rate=0.75)
                cr = creature.Creature(1)
                cr.update_dna(dna)
                new_creatures.append(cr)
            # elitism
            max_fit = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == max_fit:
                    new_cr = creature.Creature(1)
                    new_cr.update_dna(cr.dna)
                    new_creatures[0] = new_cr
                    filename = str(iteration)+"_elite"+".csv"
                    genome.Genome.to_csv(cr.dna, filename)
                    break
            
            pop.creatures = new_creatures
                            
        self.assertNotEqual(fits[0], 0)

unittest.main()
