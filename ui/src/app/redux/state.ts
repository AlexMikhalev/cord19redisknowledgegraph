export interface INode {
    id: string,
    name: string,
    rank: string
}

export interface ILink {
    source: string,
    target: string
}

export interface IEdge{
    Study: string,
    Excerpt: string
}

export interface ISearchResult{
    nodes: INode[],
    links: ILink[],
    years: any[]
}

export interface AppState {
    isLoading: boolean;
    error: any;
    searchTerm: string,
    searchResults: { search_result: ISearchResult };
    searchYears: any;
    edgeResults: IEdge[];
    nodeResults: any;
    toolBarStyle: string;
    mobile: boolean;
    sidebar: boolean;
    selected: any;
}

export const initialState: AppState = {
    isLoading: false,
    error: null,
    searchTerm:'',
    searchResults: null,
    searchYears: null,
    edgeResults: [],
    nodeResults: null,
    toolBarStyle: 'dark',
    mobile: false,
    sidebar: null,
    selected: null
};

export interface State {
    app: AppState;
}