<template>
  <component :is="component" />
</template>

<script>
import ContentWrappingCard from './ContentWrappingCard.vue';
import CustomActionsCard from './CustomActionsCard.vue';
import GridsCard from './GridsCard.vue';
import HorizontalCard from './HorizontalCard.vue';
import InformationCard from './InformationCard.vue';
import LoadingCard from './LoadingCard.vue';
import MediaWithTextCard from './MediaWithTextCard.vue';
import MiscCard from './MiscCard.vue';
import OutlinedCard from './OutlinedCard.vue';
import TwitterCard from './TwitterCard.vue';
import WeatherCard from './WeatherCard.vue';

const variants = [
    ContentWrappingCard,
    CustomActionsCard,
    GridsCard,
    HorizontalCard,
    InformationCard,
    LoadingCard,
    MediaWithTextCard,
    MiscCard,
    OutlinedCard,
    TwitterCard,
    WeatherCard,
];

export default {
  name: "JdiCard",

  components: {
    ...variants,
  },

  props: {
    data: {
        type: Object,
        default: () => ({
            type: 0,
        })
    },
  },

  computed: {
    component() {
      return variants[this.data.type];
    },
  },
};
</script>

<style></style>
