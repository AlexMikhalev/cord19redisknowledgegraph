import { createSelector, createFeatureSelector } from '@ngrx/store';

import { AppState, State } from './state';
// selectors
// export const selectAppState = createFeatureSelector<AppState>('app');
export const selectAppState = (state: State) => state.app;

export const selectSearchResults= createSelector(
    selectAppState,
    (state: AppState) => {
        return state.searchResults;
    });

export const selectEdgeResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.edgeResults;
    });

export const selectIsLoading = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.isLoading;
    });

export const selectError = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.error;
    });

export const selectNodeResults = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.nodeResults;
    });

export const selectedEvent = createSelector(
    selectAppState,
    (state: AppState) => {
        return state.selected;
    });

export const selectUX = createSelector(
    selectAppState,
    (state: AppState) => {
        return { 
            toolBarStyle: state.toolBarStyle,
            mobile: state.mobile,
            sidebar: state.sidebar
        };
    });

