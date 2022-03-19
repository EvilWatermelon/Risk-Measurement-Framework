from art.attacks.poisoning import PoisoningAttackBackdoor, PoisoningAttackCleanLabelBackdoor

# Executing the PoisoningAttackCleanLabelBackdoor attack
def clean_label(pattern):
    backdoor = PoisoningAttackBackdoor(pattern)
    attack = PoisoningAttackCleanLabelBackdoor(backdoor=backdoor, proxy_classifier=proxy.get_classifier(),
                                           target=targets, pp_poison=percent_poison, norm=2, eps=5,
                                           eps_step=0.1, max_iter=200)

# Executing the PoisoningAttackBackdoor
def art_poison_backdoor_attack(perturbation, x, y, broadcast):
    backdoor_class = PoisoningAttackBackdoor(perturbation)
    backdoor_class.poison(x, y, broadcast)
