import pandas as pd
import numpy as np

from core import *


class sample(object):
    """ WORK IN PROGRESS.
    The sample class stores compositional information for samples, and contains methods
    for normalization and other compositional calculations.
    """

    def __init__(self, composition, type='wtpt_oxides', default_normalization='none', default_type='wtpt_oxides'):
        """ Initialises the sample class.

        The composition is stored as wtpt. If the composition
        is provided as wtpt, no normalization will be applied. If the composition is supplied as
        mols, the composition will be normalized to 100 wt%.

        Parameters
        ----------
        composition     dict or pandas.Series
            The composition of the sample in the format specified by the composition_type
            parameter. Defulat is oxides in wtpt.

        type     str
            Specifies the units and type of compositional information passed in the
            composition parameter. Choose from 'wtpt_oxides', 'mol_oxides', 'mol_cations'.

        default_normalization:     None or str
            The type of normalization to apply to the data by default. One of:
                - None (no normalization)
                - 'standard' (default): Normalizes an input composition to 100%.
                - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
                The volatile wt% will remain fixed, whilst the other major element oxides are reduced
                proportionally so that the total is 100 wt%.
                - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
                volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
                be retained in addition to the normalized non-volatile oxides, summing to >100%.

        default_type     str
            The type of composition to return by default, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO
        """

        composition = composition.copy()

        if type == 'wtpt_oxides':
            self._composition = composition
        elif type == 'mol_oxides':
            self._composition = self._molOxides_to_wtpercentOxides(composition)
        elif type == 'mol_cations':
            self._composition = self._molCations_to_wtpercentOxides(composition)
        else:
            raise InputError("Type must be one of 'wtpt_oxides', 'mol_oxides', or 'mol_cations'.")

        self.set_default_normalization(default_normalization)
        self.set_default_type(default_type)


    def set_default_normalization(self, default_normalization):
        """ Set the default type of normalization to use with the get_composition() method.

        Parameters
        ----------
        default_normalization:    str
            The type of normalization to apply to the data. One of:
                - 'none' (no normalization)
                - 'standard' (default): Normalizes an input composition to 100%.
                - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
                The volatile wt% will remain fixed, whilst the other major element oxides are reduced
                proportionally so that the total is 100 wt%.
                - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
                volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
                be retained in addition to the normalized non-volatile oxides, summing to >100%.
        """
        if default_normalization in ['none','standard','fixedvolatiles','additionalvolatiles']:
            self.default_normalization = default_normalization
        else:
            raise InputError("The normalization method must be one of 'none', 'standard', 'fixedvolatiles',\
             or 'additionalvolatiles'.")

    def set_default_type(self, default_type):
        """ Set the default type of composition to return when using the get_composition() method.

        Parameters
        ----------
        default_type     str
            The type of composition to return, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO
        """
        if default_type in ['wtpt_oxides','mol_oxides','mol_cations','mol_singleO']:
            self.default_type = default_type
        else:
            raise InputError("The type must be one of 'wtpt_oxides','mol_oxides','mol_cations','mol_singleO'.")


    def get_composition(self, normalization=None, type=None, exclude_volatiles=False):
        """ Returns the composition in the format requested, normalized as requested.

        Parameters
        ----------
        normalization:     NoneType or str
            The type of normalization to apply to the data. One of:
                - 'none' (no normalization)
                - 'standard' (default): Normalizes an input composition to 100%.
                - 'fixedvolatiles': Normalizes major element oxides to 100 wt%, including volatiles.
                The volatile wt% will remain fixed, whilst the other major element oxides are reduced
                proportionally so that the total is 100 wt%.
                - 'additionalvolatiles': Normalises major element oxide wt% to 100%, assuming it is
                volatile-free. If H2O or CO2 are passed to the function, their un-normalized values will
                be retained in addition to the normalized non-volatile oxides, summing to >100%.
            If NoneType is passed the default normalization option will be used (self.default_normalization).

        type:     NoneType or str
            The type of composition to return, one of:
            - wtpt_oxides (default)
            - mol_oxides
            - mol_cations
            - mol_singleO
            If NoneType is passed the default type option will be used (self.default_type).

        exclude_volatiles   bool
            If True, volatiles will be excluded from the returned composition, prior to normalization and
            conversion.

        Returns
        -------
        dict
            The sample composition, as specified.
        """

        # Fetch the default return types if not specified in function call
        if normalization == None:
            normalization = self.default_normalization
        if type == None:
            type = self.default_type

        if exclude_volatiles == True:
            composition = self._composition.copy()
            if 'H2O' in composition.index:
                composition = composition.drop(index='H2O')
            if 'CO2' in composition.index:
                composition = composition.drop(index='CO2')
        else:
            composition = self._composition

        # Do requested normalization
        if normalization == 'none':
            normed = composition
        elif normalization == 'standard':
            normed = self._normalize_Standard(composition)
        elif normalization == 'fixedvolatiles':
            normed = self._normalize_FixedVolatiles(composition)
        elif normalization == 'additionalvolatiles':
            normed = self._normalize_AdditionalVolatiles(composition)
        else:
            raise InputError("The normalization method must be one of 'none', 'standard', 'fixedvolatiles',\
             or 'additionalvolatiles'.")

        # Get the requested type of composition
        if type == 'wtpt_oxides':
            return normed
        elif type == 'mol_oxides':
            return self._wtpercentOxides_to_molOxides(composition)
        elif type == 'mol_cations':
            return self._wtpercentOxides_to_molCations(composition)
        elif type == 'mol_singleO':
            return self._wtpercentOxides_to_molSingleO(composition)
        else:
            raise InputError("The type must be one of 'wtpt_oxides', 'mol_oxides', 'mol_cations', \
            or 'mol_singleO'.")


    def get_formulaweight(self,exclude_volatiles=False):
        """ Converts major element oxides in wt% to the formula weight (on a 1 oxygen basis).

        Parameters
        ----------
        exclude_volatiles   bool
            If True the formula weight will be calculated without volatiles

        Returns
        -------
        float
            The formula weight of the composition, on a one oxygen basis.
        """

        cations = self.get_composition(type='mol_singleO',exclude_volatiles=exclude_volatiles)

        if type(cations) != dict:
            cations = dict(cations)

        FW = 15.999
        for cation in list(cations.keys()):
            FW += cations[cation]*CationMass[cations_to_oxides[cation]]

        return FW

    def _normalize_Standard(self, composition):
        """
        Normalizes the given composition to 100 wt%, including volatiles. This method
        is intended only to be called by the get_composition() method.

        Parameters
        ----------
        composition:     pandas.Series
            A rock composition with oxide names as keys and wt% concentrations as values.

        Returns
        -------
        pandas.Series
            Normalized oxides in wt%.
        """
        comp = composition.copy()
        comp = dict(comp)
        return pd.Series({k: 100.0 * v / sum(comp.values()) for k, v in comp.items()})

    def _normalize_FixedVolatiles(self, composition):
        """
        Normalizes major element oxides to 100 wt%, including volatiles. The volatile
        wt% will remain fixed, whilst the other major element oxides are reduced proportionally
        so that the total is 100 wt%.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition:     pandas Series
            Major element oxides in wt%

        Returns
        -------
        pandas Series
            Normalized major element oxides.
        """
        comp = composition.copy()
        normalized = pd.Series({},dtype=float)
        volatiles = 0
        if 'CO2' in list(comp.index):
            volatiles += comp['CO2']
        if 'H2O' in list(comp.index):
            volatiles += comp['H2O']

        for ox in list(comp.index):
            if ox != 'H2O' and ox != 'CO2':
                normalized[ox] = comp[ox]

        normalized = normalized/np.sum(normalized)*(100-volatiles)

        if 'CO2' in list(comp.index):
            normalized['CO2'] = comp['CO2']
        if 'H2O' in list(comp.index):
            normalized['H2O'] = comp['H2O']

        return normalized

    def _normalize_AdditionalVolatiles(self, composition):
        """
        Normalises major element oxide wt% to 100%, assuming it is volatile-free. If
        H2O or CO2 are passed to the function, their un-normalized values will be retained
        in addition to the normalized non-volatile oxides, summing to >100%.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        sample:     pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            Normalized major element oxides.
        """
        comp = composition.copy()
        normalized = pd.Series({}, dtype=float)
        for ox in list(comp.index):
            if ox != 'H2O' and ox != 'CO2':
                normalized[ox] = comp[ox]

        normalized = normalized/np.sum(normalized)*100
        if 'H2O' in comp.index:
            normalized['H2O'] = comp['H2O']
        if 'CO2' in comp.index:
            normalized['CO2'] = comp['CO2']

        return normalized

    def _wtpercentOxides_to_molOxides(self, composition):
        """
        Converts a wt% oxide composition to mol oxides, normalised to 1 mol.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition:    pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            Molar proportions of major element oxides, normalised to 1.
        """
        molOxides = {}
        comp = composition.copy()
        oxideslist = list(comp.index)

        for ox in oxideslist:
            molOxides[ox] = comp[ox]/oxideMass[ox]

        molOxides = pd.Series(molOxides)
        molOxides = molOxides/molOxides.sum()

        return molOxides

    def _wtpercentOxides_to_molCations(self, composition):
        """
        Converts a wt% oxide composition to molar proportions of cations (normalised to 1).

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition        pandas.Series
            Major element oxides in wt%.

        Returns
        -------
        pandas.Series
            Molar proportions of cations, normalised to 1.
        """
        molCations = {}
        comp = composition.copy()
        oxideslist = list(comp.index)

        for ox in oxideslist:
            cation = oxides_to_cations[ox]
            molCations[cation] = CationNum[ox]*comp[ox]/oxideMass[ox]

        molCations = pd.Series(molCations)
        molCations = molCations/molCations.sum()

        return molCations

    def _wtpercentOxides_to_molSingleO(self, composition):
        """
        Constructs the chemical formula, on a single oxygen basis, from wt% oxides.

        Intended to be called only by the get_composition() method.

        Parameters
        ----------
        composition        pandas.Series
            Major element oxides in wt%

        Returns
        -------
        pandas.Series
            The chemical formula of the composition, on a single oxygen basis. Each element is
            a separate entry in the Series.
        """
        molCations = {}
        comp = composition.copy()

        oxideslist = list(comp.index)

        total_O = 0.0
        for ox in oxideslist:
            cation = oxides_to_cations[ox]
            molCations[cation] = CationNum[ox]*comp[ox]/oxideMass[ox]
            total_O += OxygenNum[ox]*comp[ox]/oxideMass[ox]

        molCations = pd.Series(molCations)
        molCations = molCations/total_O

        return molCations

    def _molOxides_to_wtpercentOxides(self, composition):
        """
        Converts mol oxides to wt% oxides. Returned composition is normalized to 100 wt%.

        Parameters
        ----------
        composition:     pandas.Series
            mol fraction oxides

        Returns
        -------
        pandas.Series
            wt% oxides normalized to 100 wt%.
        """

        comp = composition.copy()
        wtpt = {}

        for ox in composition.index:
            wtpt[ox] = comp[ox]*oxideMass[ox]

        wtpt = pd.Series(wtpt)
        wtpt = wtpt/wtpt.sum()*100

        return wtpt

    def _molOxides_to_molCations(self, composition):
        """
        Converts mol oxides to mol cations. Returned composition is normalized to 1 mol
        cations.

        Parameters
        ----------
        composition:     pandas.Series
            mole fraction oxides

        Returns
        -------
        pandas.Series
            mole fraction cations
        """

        comp = composition.copy()
        molcations = {}

        for ox in comp.index:
            molcations[oxides_to_cations[ox]] = comp[ox]*CationNum[ox]

        molcations = pd.Series(molcations)
        molcations = molcations/molcations.sum()

        return molcations

    def _molCations_to_wtpercentOxides(self, composition):
        """
        Converts mole fraction cations to wt% oxides, normalized to 100 wt%.

        Parameters
        ----------
        composition:     pandas.Series
            Mole fraction cations

        Returns
        -------
        pandas.Series
            Wt% oxides, normalized to 100 wt%.
        """

        comp = composition.copy()
        wtpt = {}

        for el in comp.index:
            wtpt[cations_to_oxides[el]] = comp[el]/CationNum[cations_to_oxides[el]]*oxideMass[cations_to_oxides[el]]

        wtpt = pd.Series(wtpt)
        wtpt = wtpt/wtpt.sum()*100

        return wtpt

    def _molCations_to_molOxides(self, composition):
        """
        Converts mole fraction cations to mole fraction oxides, normalized to 1 mole.

        Parameters
        ----------
        composition:     pandas.Series
            Mole fraction cations

        Returns
        -------
        pandas.Series
            Mole fraction oxides, normalized to one.
        """
        comp = composition.copy()
        moloxides = {}

        for el in comp.index:
            moloxides[cations_to_oxides[el]] = comp[el]/CationNum[cations_to_oxides[el]]

        moloxides = pd.Series(moloxides)
        moloxides = moloxides/moloxides.sum()

        return moloxides