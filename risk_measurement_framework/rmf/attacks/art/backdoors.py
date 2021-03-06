from art.attacks.poisoning import *
from art import *
from art.attacks.poisoning.perturbations import insert_image, add_pattern_bd

import matplotlib.pyplot as plt
import numpy as np

from measurement import monitoring

def poison_func(x):
    return insert_image(x, backdoor_path='../rmf/backdoors/alert.png',
                        size=(10, 10), mode='RGB', blend=0.8, random=True)

def mod(x):

    patch_size = 8
    x_shift = 32 - patch_size - 5
    y_shift = 32 - patch_size - 5

    original_dtype = x.dtype
    x = insert_image(x, backdoor_path='../rmf/backdoors/htbd.png',
                     channels_first=False, random=False, x_shift=x_shift, y_shift=y_shift,
                     size=(patch_size, patch_size), mode='RGB', blend=1)
    return x.astype(original_dtype)

# Executing the PoisoningAttackCleanLabelBackdoor attack (black-box)
def clean_label(x, y, clf, target_label, poison_number):
    """
    https://people.csail.mit.edu/madry/lab/cleanlabel.pdf
    """

    print("Execute clean label backdoor attack...")
    backdoor = PoisoningAttackBackdoor(mod)
    attack = PoisoningAttackCleanLabelBackdoor(backdoor=backdoor, proxy_classifier=clf,
                                               target=target_label, pp_poison=poison_number, norm=2, eps=5,
                                               eps_step=0.1, max_iter=200)

    poison_data, poison_labels = attack.poison(x, y)
    print("Finished poisoning!")

    return poison_data, poison_labels, backdoor

# Untargeted attack (black-box)
def art_poison_backdoor_attack(x, y, num_of_images):
    """
    https://arxiv.org/abs/1708.06733
    """

    backdoor_class = PoisoningAttackBackdoor(poison_func)
    poisoned_data, poisoned_y = backdoor_class.poison(x[:num_of_images], y[:num_of_images])

    print("Finished poisoning!")

    return poisoned_data, poisoned_y

# Targeted attack (white-box)
def art_hidden_trigger_backdoor(x, y, target, source):
    """
    https://arxiv.org/pdf/1910.00033.pdf
    """

    print("Execute hidden trigger backdoor attack...")
    backdoor = PoisoningAttackBackdoor(mod)

    poison_attack = HiddenTriggerBackdoor(classifier, eps=16/255, target=target, source=source, feature_layer=9, backdoor=backdoor,
                                          learning_rate=0.01, decay_coeff = .1, decay_iter = 1000, max_iter=3000, batch_size=25, poison_percent=.15)

    poison_data, poison_labels = poison_attack.poison(x, y)
    print("Finished poisoning!")

    return poison_data, poison_labels
