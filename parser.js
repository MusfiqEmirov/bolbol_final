const categoryData = { 
    /* Your JSON data here */
};

// Function to extract all parent categories
function getParentCategories(data) {
    return Object.keys(data);
}

// Function to extract subcategories for a given parent category
function getSubcategories(parentCategory, data) {
    if (data[parentCategory] && data[parentCategory].subcategories) {
        return Object.keys(data[parentCategory].subcategories);
    }
    return [];
}

// Recursive function to extract filters for a subcategory
function getFilters(subcategoryData) {
    let filters = {};

    // Extract default filters
    if (subcategoryData.defaultFilters) {
        filters["defaultFilters"] = subcategoryData.defaultFilters;
    }

    // Extract subcategory filters (with recursion)
    if (subcategoryData.subcategoryFilters) {
        filters["subcategoryFilters"] = {};
        for (const [key, value] of Object.entries(subcategoryData.subcategoryFilters)) {
            filters["subcategoryFilters"][key] = processInnerFilters(value);
        }
    }

    return filters;
}

// Recursive function to process inner filters
function processInnerFilters(filterData) {
    let result = {};

    // Copy type & useForProductName if exists
    if (filterData.type) {
        result["type"] = filterData.type;
    }
    if (filterData.useForProductName) {
        result["useForProductName"] = filterData.useForProductName;
    }

    // Process choices recursively
    if (filterData.choices) {
        result["choices"] = {};
        for (const [choiceKey, choiceValue] of Object.entries(filterData.choices)) {
            result["choices"][choiceKey] = choiceValue.innerFilters 
                ? processInnerFilters(choiceValue.innerFilters) 
                : null;
        }
    }

    return result;
}

// Function to extract filters for a specific subcategory
function getSubcategoryFilters(parentCategory, subcategory, data) {
    if (data[parentCategory] && data[parentCategory].subcategories) {
        let subcategoryData = data[parentCategory].subcategories[subcategory];
        if (subcategoryData) {
            return getFilters(subcategoryData);
        }
    }
    return null;
}

// Example Usage:
console.log("Parent Categories:", getParentCategories(categoryData));  
console.log("Subcategories in 'Elektronika':", getSubcategories("Elektronika", categoryData));  
console.log("Filters for 'Telefonlar':", getSubcategoryFilters("Elektronika", "Telefonlar", categoryData));  