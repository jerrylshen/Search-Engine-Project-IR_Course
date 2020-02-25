$("#buttonSelector").click(function () 
{
     $(this).button('loading');
     // Long waiting operation here
     $(this).button('reset');
}
);