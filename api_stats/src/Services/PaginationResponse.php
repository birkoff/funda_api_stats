<?php

namespace Funda\Services;

class PaginationResponse
{
    public static function getPaginationValues($url = '', $page = 1, $totalItems = 1, $maxResults = 25)
    {
        $lastPage = $totalItems/$maxResults;
        $next = self::getNextPage($page, $lastPage);
        $prev = self::getPrevPage($page);

        return [
            'current' => $page,
            'next' => $next ? $url . $next : 0,
            'prev' => $prev ? $url . $prev : 0,
            'total' => ceil($lastPage)
        ];
    }

    private static function getNextPage($page, $lastPage)
    {
        return ($page + 1) <= $lastPage ? ($page + 1) : 0;
    }

    private static function getPrevPage($page)
    {
        return ($page - 1) <= 0 ? 0 : $page - 1;
    }
}