const userInfoReducer = (
    state = {
      brand: [],
      address: null,
      location: []
},
    action,
  ) => {
    switch (action.type) {
      case 'ADD_BRAND':
        return { ...state, brand: [...state.brand, action.payload] };
      case 'REMOVE_BRAND':
        return { ...state, brand: [...state.brand].filter(brand => brand !== action.payload) };
      case 'SET_ADDRESS':
        return { ...state, address: action.payload };
      case 'SET_LOCATION':
        return { ...state, location: action.payload };
      default:
        return state;
    }
  };

export default userInfoReducer;
  