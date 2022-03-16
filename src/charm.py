#!/usr/bin/env python3
"""Charm code for Awesome service."""
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.
import random
import logging
from typing import Optional

import ops.charm
from ops.main import main
from ops.model import (
    ActiveStatus,
    Relation
)

logger = logging.getLogger(__name__)

PEER = "awesome"


class AwesomeOperatorCharm(ops.charm.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.awesome_relation_joined, self._on_awesome_relation_joined)

    def _on_awesome_relation_joined(self, event: ops.charm.RelationJoinedEvent) -> None:
        """Adds the peer unit in an awesome way

        Args:
            event: The triggering relation joined/changed event.
        """

        # only allow the leader to execute code
        if not self.unit.is_leader():
            logger.debug("unit %s is not leader, returning...", self.unit.name)
            return

        # helpful message
        logger.debug("Adding a unit %s", event.unit.name)

        # do some computation that is crucial for the user to know
        # grab the data from peer unit
        unit_number = int(self._peers.data[self.unit]["special_number"])
        useful_math = unit_number/0  # code that will cause an error, to be resolved in juju debug-hooks session
        logger.debug("This unit number divided by 10 is %s", useful_math)

    def _on_start(self, event: ops.charm.StartEvent) -> None:
        """Enables awesome service and initialises data.

        Args:
            event: The triggering start event.
        """
        # helpful message
        logger.debug("Starting unit %s", self.unit.name)

        # set up our extremely useful data
        unit_data = random.randint(0, 10)

        # relation data must be strings
        self._peers.data[self.unit].update({"special_number": str(unit_data)})
        logger.debug("unit: %s has the random number %s", self.unit.name, unit_data)

        # unit is ready to go
        self.unit.status = ActiveStatus()

    @property
    def _peers(self) -> Optional[Relation]:
        """Fetch the peer relation.

        Returns:
             An `ops.model.Relation` object representing the peer relation.
        """
        return self.model.get_relation(PEER)


if __name__ == "__main__":
    main(AwesomeOperatorCharm)
