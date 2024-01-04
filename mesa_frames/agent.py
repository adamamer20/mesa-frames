import pandas as pd
from numpy.random import randint
from mesa_frames.model import ModelDF

class AgentDF:
    """The AgentDF class is the base class for other agents.
    It should be used as inherited class for new agents classes.

    Attributes:
    ----------
    dtypes : dict[str, str]
        The data types of the attributes of the Agent. Default: {'id' : 'int64', 'type' : 'str'}
    model : Model
        The model of the simulation where the Agent is used. See src/model.py. Default: None
    mask : pd.Series
        The mask of the agents dataframe in the model which corresponds to the Agent class.
        Initialized when model is created. Default: None

    Methods:
    --------
    Methods should be decorated as @classmethod and should act on the mask portion of the agents dataframe of the model.

    __init__():
        Initializes the Agent class.
        Assigns a 64-bit random id to each agent in the model.

    step():
        The step method of the Agent class.
        It should be decorated as @classmethod and should act on the mask portion of the agents dataframe of the model.

    """

    dtypes: dict[str, str] = {
        "id": "int64",
        "type": "str",
    }
    model: ModelDF | None = None
    mask: pd.Series | None = None

    @classmethod
    def __init__(cls):
        """Initializes the Agent class.
        Assigns a 64-bit random id to each agent in the model.
        """
        if cls.mask is None or cls.model is None or cls.model.agents is None:
            raise ValueError(
                "The Agent classes have not been initialized. Please use the model.create_agents() method to initialize the mask."
            )
        cls.model.agents.loc[cls.mask, "id"] = randint(
            low=-9223372036854775808,
            high=9223372036854775807,
            size=cls.mask.sum(),
            dtype="int64",
        )

    @classmethod
    def step(cls):
        """The step method of the Agent class.
        It should be decorated as @classmethod and should act on the mask portion of the agents dataframe of the model.
        """
        raise NotImplementedError


class GeoAgentDF(AgentDF):
    """The GeoAgentDF extends the AgentDF class to include a geometry attribute.
    The agents will be stored in a GeoDataFrame."""

    dtypes: dict[str, str] = {"geometry": "geometry"}

    @classmethod
    def step(cls):
        """The step method of the GeoAgentDF class.
        It should act on the mask portion of the agents dataframe of the model.
        """
        raise NotImplementedError